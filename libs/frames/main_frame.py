
import pydicom
import os
import numpy as np
import datetime as dt
import cv2 
import random

from tkinter import Frame, Label, Button, Entry, filedialog, END, Toplevel, \
    Canvas, Listbox, Scale
from PIL import ImageTk, Image


from .info_frame import info_frame
from ..methods import find_real_rois, find_simu_rois, readDicom


class MainFrame(Frame):
    def __init__(self, root):

        self.root = root

        root_init_2afc = Toplevel(self.root)

        root_init_2afc.title("Info")
        root_init_2afc.geometry("305x452")
        root_init_2afc.minsize(width=305, height=452)
        root_init_2afc.maxsize(width=305, height=452)

        infoFrame = info_frame(root_init_2afc, self)

        root_init_2afc.protocol("WM_DELETE_WINDOW", infoFrame.on_closing)
        
        ##########################################
        # Frames
        ##########################################

        self.build_frames()

        self.build_top_frame()
        self.build_btm_frame()

        ##########################################
        # Variables
        ##########################################
        
        self.img_ind = 0
        
        self.real_imgs_paths = find_real_rois()
        self.fake_imgs_paths = find_simu_rois()
        
        random.shuffle(self.real_imgs_paths)
        random.shuffle(self.fake_imgs_paths)
        
        self.real_imgs_paths = self.real_imgs_paths[:100]
        self.fake_imgs_paths = self.fake_imgs_paths[:100]
        # print(len(self.real_imgs_paths),len(self.fake_imgs_paths))
        self.where_is_fake = []
        self.where_user_clicked = []
        
        self.img_on_left = None
        self.img_on_right = None

        ##########################################
        # Startup functions
        ##########################################
        
        self.get_next_images()


    def build_frames(self):

        self.top_frame = Frame(self.root)
        self.btm_frame = Frame(self.root)

        # Palce it on a grid
        self.top_frame.grid(row=0)
        self.btm_frame.grid(row=1)
        

    def build_top_frame(self):
        

        # Tmp image just to get space
        img = np.zeros((200,200)).astype(np.uint8) * 128
        img2plot = ImageTk.PhotoImage(image=Image.fromarray(img))

        self.img_panel_left = Label(self.btm_frame, image=img2plot)
        self.img_panel_right = Label(self.btm_frame, image=img2plot)
        
        self.left_scrollbar = Scale(self.btm_frame, orient='horizontal', from_=0, to=14, resolution=1,showvalue=False, command=lambda pos, name='left': self.get_next_slice(pos, name))
        self.right_scrollbar = Scale(self.btm_frame, orient='horizontal', from_=0, to=14, resolution=1,showvalue=False, command=lambda pos, name='right': self.get_next_slice(pos, name))
          

        self.img_panel_left.grid(row=0, column=0, columnspan=1)
        self.img_panel_right.grid(row=0, column=1, columnspan=1)
        
        self.left_scrollbar.grid(row=1, column=0, columnspan=1, sticky='EW')
        self.right_scrollbar.grid(row=1, column=1, columnspan=1, sticky='EW')
        
        
    def build_btm_frame(self):

        # Button Widget
        button_left  = Button(self.top_frame, text="This is real", width = 20, height=2, command=self.func_button_left)
        button_right = Button(self.top_frame, text="This is real", width = 20, height=2, command=self.func_button_right)
        # button_print = Button(self.top_frame, text="print", width = 20, height=2, command=self.func_button_print)


        button_left.grid(row=0, column=0, columnspan=1)
        button_right.grid(row=0, column=1, columnspan=1)
        # button_print.grid(row=1, column=0, columnspan=1)

        return

    ########## Button func ##########


    def func_button_left(self):
        
        self.where_user_clicked.append(1)
        # print(self.where_user_clicked, self.where_is_fake)
        # if self.where_user_clicked[-1] == self.where_is_fake[-1]:
        #     print("Wrong")
        # else:
        #     print("Correct")
        self.get_next_images()

        return

    def func_button_right(self):
    
        self.where_user_clicked.append(0)
        # print(self.where_user_clicked, self.where_is_fake)
        # if self.where_user_clicked[-1] == self.where_is_fake[-1]:
        #     print("Wrong")
        # else:
        #     print("Correct")
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
        img = np.uint8(img)
        
        return img
    
    def get_next_images(self):
        
        # print(self.real_imgs_paths[self.img_ind], self.fake_imgs_paths[self.img_ind])
        
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
        
        if name == 'left':
            self.show_img(self.img_on_left[..., int(pos)], self.img_panel_left)
        else:
            self.show_img(self.img_on_right[..., int(pos)], self.img_panel_right)
            
        return


