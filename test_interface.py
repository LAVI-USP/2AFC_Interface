# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:28:26 2022

@author: Arthur C. Costa

Reproducing a GUI for the 2AFC test in python
"""

from tkinter import Frame, Button, Entry, Label, Tk, filedialog
# from tkinter import ttk
import os
import datetime as dt
# import pandas as pd
# from pydicom import dcmread

class Application(Frame):
    def __init__(self, master=None):

        self.root = master
        self.name = []
        self.createWidgets()

    def get_readername(self): # No getting entry_name

        self.name = self.entry_name.get()
        user_folder = './Results/'+self.name
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        creation_date = dt.datetime.now()
        creation_date = creation_date.strftime("%d/%m/%Y %H:%M")
        # Temporary alternative just to test the txt creation
        user_code = ('Reader: {}'.format(self.name), creation_date)
        with open(os.path.join(user_folder,'results.txt'), 'w') as f:
            f.write(' '.join(str(s) for s in user_code) + '\n')
        
    def run(self):

        if not self.name:    

            raise ValueError('Error, please type a name to identify yourself.')

            return
        

    def createWidgets(self):
        
        self.QUIT = Button(self.root, text="QUIT", command=self.root.quit) # Not working properly
        self.first_txt  = Label(self.root,text='Please insert your name:')
        self.entry_name = Entry()
        self.startButton = Button(self.root, text="START", command=self.get_readername())
        
        self.QUIT.grid(row=0, column=0)
        self.first_txt.grid(column=0,row=1,padx=10,pady=10,sticky='nswe',columnspan=4)
        self.entry_name.grid(column=0,row=2,padx=10,pady=10,sticky='nswe',columnspan=4)
        self.startButton.grid(column=0,row=3,padx=10,pady=10,sticky='nswe',columnspan=2)
        

root = Tk()
root.title("Reader Information")

app = Application(master=root)
root.mainloop()