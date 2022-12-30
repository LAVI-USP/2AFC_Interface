
import os
import cv2
import numpy as np
import random

from tkinter import Frame, Label, Button, Entry, filedialog, END, Toplevel, \
    Canvas, Listbox, Scale
from PIL import ImageTk, Image

from ..utils.methods import find_real_rois, find_simu_rois, readDicom


class twoafc_frame(Frame):

    def __init__(self, root, mainFrame):

        self.root = root
        self.mainFrame = mainFrame

        ##########################################
        # Variables
        ##########################################
        
        self.img_ind = 0
        
        self.real_imgs_paths = find_real_rois()
        self.fake_imgs_paths = find_simu_rois()
        
        # print(len(self.real_imgs_paths),len(self.fake_imgs_paths))

        self.real_imgs_paths = self.real_imgs_paths[:100]
        self.fake_imgs_paths = self.fake_imgs_paths[:100]

        random.shuffle(self.real_imgs_paths)
        random.shuffle(self.fake_imgs_paths)

        self.where_is_fake = []
        self.where_user_clicked = []
        
        self.img_on_left = None
        self.img_on_right = None
        
        ##########################################
        # Frames
        ##########################################

        self.flag_info_ok = 1
        self.build_frames()
        self.get_next_images()

        return
        

    def build_frames(self):

        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()

        self.root.geometry("{}x{}".format(screenwidth, screenheight))

        self.root.configure(background='black')

        self.top_frame = Frame(self.root, width=screenwidth, height=200, bg = "black", highlightthickness=0)
        # self.top_frame.grid_propagate(0)
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.rowconfigure(1, weight=1)
        self.btm_frame = Frame(self.root, width=screenwidth, height=850, bg = "black", highlightthickness=0)
        # self.btm_frame.grid_propagate(0)
        self.btm_frame.rowconfigure(0, weight=1)
        self.btm_frame.rowconfigure(1, weight=1)

        # Palce it on a grid
        self.top_frame.pack(side="top", fill="y") #.grid(row=0)
        self.btm_frame.pack(side="bottom", fill="y")#.grid(row=1)

        self.build_top_frame()
        self.build_btm_frame()
        
    def build_btm_frame(self):
        

        # Tmp image just to get space
        img = np.zeros((400,400)).astype(np.uint8) * 128
        img2plot = ImageTk.PhotoImage(image=Image.fromarray(img))

        self.img_panel_left = Label(self.btm_frame, image=img2plot, bg = "black")
        self.img_panel_right = Label(self.btm_frame, image=img2plot, bg = "black")
        
        self.left_scrollbar = Scale(self.btm_frame, orient='horizontal', from_=0, to=14, resolution=1,showvalue=False, command=lambda pos, name='left': self.get_next_slice(pos, name), background='black', fg='black', troughcolor='black', activebackground='white', highlightthickness=0)
        self.right_scrollbar = Scale(self.btm_frame, orient='horizontal', from_=0, to=14, resolution=1,showvalue=False, command=lambda pos, name='right': self.get_next_slice(pos, name), background='black', fg='black', troughcolor='black', activebackground='white', highlightthickness=0)
          
        self.left_scrollbar.set(7)
        self.right_scrollbar.set(7)

        self.btm_frame.bind_all("<MouseWheel>", self._on_mousewheel)

        self.img_panel_left.grid(row=0, column=0, columnspan=1, ipady=10, sticky='NWNE', padx=(0, 10))
        self.img_panel_right.grid(row=0, column=1, columnspan=1, ipady=10, sticky='NWNE', padx=(10, 0))
        
        self.left_scrollbar.grid(row=2, column=0, columnspan=1, sticky='SWSE', ipady=80, padx=(0, 10))
        self.right_scrollbar.grid(row=2, column=1, columnspan=1, sticky='SWSE', ipady=80, padx=(10, 0))
        
    def build_top_frame(self):

        self.label = Label(self.top_frame, text = "Which image is real?", font=('TkDefaultFont',18), bg = "black", fg = "white")
        self.label_number = Label(self.top_frame, text = "1/100", font=('TkDefaultFont',12), bg = "black", fg = "white")

        # Button Widget
        button_left  = Button(self.top_frame, text="1", width=10, height=2, command=self.func_button_left, bg = "black", fg = "white")
        button_right = Button(self.top_frame, text="2", width=10, height=2, command=self.func_button_right, bg = "black", fg = "white")
        # button_print = Button(self.top_frame, text="print", width = 20, height=2, command=self.func_button_print)

        self.label.grid(row=0, column=0, columnspan=2, sticky='EW', pady=(250, 5)) 
        self.label_number.grid(row=1, column=0, columnspan=2, sticky='EW', pady=(5, 5)) 

        button_left.grid(row=2, column=0, sticky='SWSE', padx=(5, 160))
        button_right.grid(row=2, column=1, sticky='SWSE', padx=(160, 5))
        # button_print.grid(row=1, column=0, columnspan=1)

        return

    def _on_mousewheel(self, event):


        left_scrollbar_val = self.left_scrollbar.get()
        right_scrollbar_val = self.right_scrollbar.get()

        if -1*(event.delta/120) < 0:
            if left_scrollbar_val < 14:
                self.left_scrollbar.set(left_scrollbar_val + 1)
            if right_scrollbar_val < 14:
                self.right_scrollbar.set(right_scrollbar_val + 1)
        else:
            if left_scrollbar_val > 0:
                self.left_scrollbar.set(left_scrollbar_val - 1)
            if right_scrollbar_val > 0:
                self.right_scrollbar.set(right_scrollbar_val - 1)

    ########## Button func ##########


    def func_button_left(self):

        if self.flag_info_ok:
        
            self.where_user_clicked.append(1)
            # print(self.where_user_clicked, self.where_is_fake)
            # print(self.real_imgs_paths[self.img_ind-1])
            # print(self.fake_imgs_paths[self.img_ind-1])
            # if self.where_user_clicked[-1] == self.where_is_fake[-1]:
            #     print("Wrong \n")
            # else:
            #     print("Correct \n")
            self.get_next_images()

        return

    def func_button_right(self):

        if self.flag_info_ok:
    
            self.where_user_clicked.append(0)
            # print(self.where_user_clicked, self.where_is_fake)
            # print(self.real_imgs_paths[self.img_ind-1])
            # print(self.fake_imgs_paths[self.img_ind-1])
            # if self.where_user_clicked[-1] == self.where_is_fake[-1]:
            #     print("Wrong \n")
            # else:
            #     print("Correct \n")
            self.get_next_images()

        return
    
    # def func_button_print(self):
    #     print(self.real_imgs_paths[self.img_ind-1], self.fake_imgs_paths[self.img_ind-1])
    #     return
        
    ########## General func ##########
    
    
    def show_img(self, img, img_panel):
        
        img2plot = ImageTk.PhotoImage(image=Image.fromarray(img))
        
        img_panel.configure(image=img2plot)
        img_panel.image = img2plot    
        
        return
    
    def pre_process(self, img):
        
        img = (img - img.min()) / (img.max() - img.min())
        img *= 255
        img = 255 - img
        img = np.uint8(img)

        img  = cv2.resize(img, (0,0), fx=2, fy=2) 
        
        return img
    
    def get_next_images(self):
        
        if self.img_ind == 100:
            self.calc_statistcs()
            self.mainFrame.on_quit()
        else:

            # print(self.real_imgs_paths[self.img_ind], self.fake_imgs_paths[self.img_ind])

            self.label_number.config(text ="{}/100".format(self.img_ind+1))

            img_real = readDicom(self.real_imgs_paths[self.img_ind])
            img_fake = readDicom(self.fake_imgs_paths[self.img_ind])
            
            img_real = self.pre_process(img_real)
            img_fake = self.pre_process(img_fake)
            
            if np.random.uniform() > 0.5:
                # Show fake on left
                self.where_is_fake.append(1)
                self.img_on_left = img_fake
                self.img_on_right = img_real
                self.show_img(self.img_on_left[..., 7], self.img_panel_left)
                self.show_img(self.img_on_right[..., 7], self.img_panel_right)
            else:
                # Show fake on right
                self.where_is_fake.append(0)
                self.img_on_left = img_real
                self.img_on_right = img_fake
                self.show_img(self.img_on_left[..., 7], self.img_panel_left)
                self.show_img(self.img_on_right[..., 7], self.img_panel_right)
                
            self.left_scrollbar.set(7)
            self.right_scrollbar.set(7)
                
            self.img_ind += 1
   
        return
    
    def get_next_slice(self, pos, name):

        if self.flag_info_ok:
        
            if name == 'left':
                self.show_img(self.img_on_left[..., int(pos)], self.img_panel_left)
            else:
                self.show_img(self.img_on_right[..., int(pos)], self.img_panel_right)
            
        return

    def calc_statistcs(self):

        # Question: Where is the Real?
        #  --- where_user_clicked ---
        # Button Left = 1
        # Button Right = 0
        #  --- where_is_fake ---
        # Fake Left = 1
        # Fake Right = 0
        # ---------
        # Example:
        #
        # where_user_clicked = [0, 1, 0]
        # where_is_fake      = [1, 1, 0]
        # Result             = [Correct, Wrong, Wrong]

        numer_of_correct = np.size(np.where((np.array(self.where_user_clicked) ^ np.array(self.where_is_fake)) == 1)[0])

        with open(os.path.join(self.mainFrame.user_folder,'results.txt'), 'a') as f:
                f.write("Percentage of correct choices: {} \n\n Where user clicked:{} \n\n Where fake is:{}\n ".format(numer_of_correct / 100, self.where_user_clicked, self.where_is_fake))

        return
 
    def on_closing(self):

        self.root.destroy()
        self.mainFrame.on_quit()

        return

        
        