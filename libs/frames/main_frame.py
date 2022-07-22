
import pydicom
import os
import numpy as np
import datetime as dt
import cv2 

from tkinter import Frame, Label, Button, Entry, filedialog, END, Toplevel
from PIL import ImageTk, Image


from .info_frame import info_frame


class MainFrame(Frame):
    def __init__(self, root):

        self.root = root

        root_init_2afc = Toplevel(self.root)

        root_init_2afc.title("INICIAR SIMULAÇÃO")
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



    def build_frames(self):

        self.top_frame = Frame(self.root)
        self.btm_frame = Frame(self.root)

        # Palce it on a grid
        self.top_frame.grid(row=0)
        self.btm_frame.grid(row=1)

    def build_top_frame(self):

        # Tmp image just to get space
        img = np.zeros((250,250)).astype(np.uint8) * 128
        img2plot = ImageTk.PhotoImage(image=Image.fromarray(img))

        self.img_panel_left = Label(self.btm_frame, image=img2plot)
        self.img_panel_right = Label(self.btm_frame, image=img2plot)

        self.img_panel_left.grid(row=0, column=0, columnspan=1)
        self.img_panel_right.grid(row=0, column=1, columnspan=1)
 
        
    def build_btm_frame(self):

        # Button Widget
        button_left  = Button(self.top_frame, text="Select1", width = 35, height=2, command=self.func_button_left)
        button_right = Button(self.top_frame, text="Select2", width = 35, height=2, command=self.func_button_right)


        button_left.grid(row=0, column=0, columnspan=1)
        button_right.grid(row=0, column=1, columnspan=1)


        return

    ########## Button func ##########


    def func_button_left(self):

        img = np.empty((500,500)).astype(np.uint8) * 128
        img2plot = ImageTk.PhotoImage(image=Image.fromarray(img))
        
        self.img_panel_left.configure(image=img2plot)
        self.img_panel_left.image = img2plot    

        return

    def func_button_right(self):

        img = np.empty((500,500)).astype(np.uint8) * 128
        img2plot = ImageTk.PhotoImage(image=Image.fromarray(img))
        
        self.img_panel_right.configure(image=img2plot)
        self.img_panel_right.image = img2plot    

        return

        
    ########## General func ##########


