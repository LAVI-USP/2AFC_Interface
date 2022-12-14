from tkinter import Frame, Label, Button, Entry, filedialog, END, Toplevel

import os
import datetime as dt

from .twoafc_frame import twoafc_frame

class MainFrame(Frame):
    
    def __init__(self, root):

        ##########################################
        # Info FRAME
        ##########################################

        self.root = root
        self.root.title("Info")

        self.flag_info_ok = 0
        self.user_folder = None

        self.build_frame()

    def build_frame(self):
        
        self.first_txt  = Label(self.root,text='Please insert your name:')
        self.entry_name = Entry(self.root)
        self.startButton = Button(self.root, text="START", command=self.get_readername)
        self.quitButton = Button(self.root, text="QUIT", command=self.on_quit)
        
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

            self.user_folder = './data/results/{}-{}'.format(self.name, creation_date.strftime("%d_%m_%Y_%H_%M")) 

            if not os.path.exists(self.user_folder):
                os.makedirs(self.user_folder)

            # Temporary alternative just to test the txt creation
            user_code = ('Reader: {}'.format(self.name), creation_date.strftime("%d/%m/%Y %H:%M"))
            with open(os.path.join(self.user_folder,'results.txt'), 'w') as f:
                f.write(' '.join(str(s) for s in user_code) + '\n')


            ##########################################
            # 2AFC FRAME
            ##########################################

            root_init_2afc = Toplevel(self.root)

            self.twoafcFrame = twoafc_frame(root_init_2afc, self)

            root_init_2afc.protocol("WM_DELETE_WINDOW", self.twoafcFrame.on_closing)
        
            self.on_closing()

        else:
            print("No name")

        return

    def on_quit(self):

        self.root.quit()

        return

    def on_closing(self):

        self.root.withdraw()

        return


