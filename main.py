from tkinter import Menu, Tk

from libs.frames.main_frame import MainFrame

root = Tk()

# Define and configure menu
my_menu = Menu(root)
root.config(menu=my_menu)

mainframe = MainFrame(root)

# Loop
root.mainloop()