from tkinter import Frame, Label, Button, Entry, filedialog, END, Toplevel

import os
import datetime as dt

class info_frame(Frame):
    def __init__(self, root_init_2afc, mainFrame):

        self.root_init_2afc = root_init_2afc
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
        
        self.QUIT = Button(self.root_init_2afc, text="QUIT", command=self.root_init_2afc.quit) # Not working properly
        self.first_txt  = Label(self.root_init_2afc,text='Please insert your name:')
        self.entry_name = Entry(self.root_init_2afc)
        self.startButton = Button(self.root_init_2afc, text="START", command=self.get_readername())
        
        self.QUIT.grid(row=0, column=0)
        self.first_txt.grid(column=0,row=1,padx=10,pady=10,sticky='nswe',columnspan=4)
        self.entry_name.grid(column=0,row=2,padx=10,pady=10,sticky='nswe',columnspan=4)
        self.startButton.grid(column=0,row=3,padx=10,pady=10,sticky='nswe',columnspan=2)

    def on_closing(self):

        self.root_init_2afc.destroy()

        return
        