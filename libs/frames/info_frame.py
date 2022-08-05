from tkinter import Frame, Label, Button, Entry, filedialog, END, Toplevel

import os
import datetime as dt

class info_frame(Frame):
    def __init__(self, root_init_2afc, mainFrame):

        self.root_init_2afc = root_init_2afc
        self.mainFrame = mainFrame
        self.build_frame()

    def build_frame(self):
        
        self.first_txt  = Label(self.root_init_2afc,text='Please insert your name:')
        self.entry_name = Entry(self.root_init_2afc)
        self.startButton = Button(self.root_init_2afc, text="START", command=self.get_readername)
        self.quitButton = Button(self.root_init_2afc, text="QUIT", command=self.mainFrame.on_quit)
        
        self.first_txt.grid(column=0,row=0,sticky='nswe',columnspan=4)
        self.entry_name.grid(column=0,row=1,sticky='nswe',columnspan=4)
        self.startButton.grid(column=0,row=2,sticky='nswe',columnspan=4)
        self.quitButton.grid(column=0,row=3,sticky='nswe',columnspan=4)

        return

    ########## Button func ##########

    def get_readername(self): # No getting entry_name

        self.name = self.entry_name.get()

        if self.name:
        
            creation_date = dt.datetime.now()

            self.mainFrame.user_folder = './Results/{}-{}'.format(self.name, creation_date.strftime("%d_%m_%Y_%H_%M")) 

            if not os.path.exists(self.mainFrame.user_folder):
                os.makedirs(self.mainFrame.user_folder)

            # Temporary alternative just to test the txt creation
            user_code = ('Reader: {}'.format(self.name), creation_date.strftime("%d/%m/%Y %H:%M"))
            with open(os.path.join(self.mainFrame.user_folder,'results.txt'), 'w') as f:
                f.write(' '.join(str(s) for s in user_code) + '\n')

            self.mainFrame.get_next_images()
            self.mainFrame.flag_info_ok = 1
            self.on_closing()

        else:
            print("No name")

        return

    def on_closing(self):

        self.root_init_2afc.destroy()

        return
        