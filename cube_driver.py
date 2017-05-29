from tkinter import Tk
from interface import MainView
from person import Person

person = Person
root = Tk()
main = MainView(root)
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("800x500")
root.minsize(800, 500)
root.mainloop()