import os

from tkinter import Menu, Tk

from libs.frames.main_frame import MainFrame

# Ser working dir to the one of main.py
os.chdir(os.path.dirname(os.path.realpath(__file__)))

root = Tk()

mainframe = MainFrame(root)

# Loop
root.mainloop()