from tkinter import *
from tkinter import ttk

class MainWindow(ttk.Frame):
    def __init__(self, master):
        self.master = master 
        self.frame = ttk.Frame(self.master)        
        self.entry = ttk.Entry(self.frame)
        self.enter = ttk.Button(self.frame, text="Find Urls")
        self.list = Listbox(self.frame)
        self.entry.grid(row=0, column=0)
        self.enter.grid(row=0,column=1)
        self.list.grid(row=1, columnspan=2)
        self.frame.pack()
        self.populate_list()

    def populate_list(self):
        for num in range(10):
            self.list.insert(END, num)

if __name__ == '__main__':
    root = Tk()
    app = MainWindow(root)
    root.mainloop()