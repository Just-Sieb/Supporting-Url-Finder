from tkinter import *
from tkinter import ttk

class MainWindow(ttk.Frame):
    def __init__(self, master):
        self.master = master 
        self.master.title(string="URL Finder")
        self.master.minsize(width=250, height=300)
        self.master.maxsize(width=250, height=300)

        self.frame = ttk.Frame(self.master)        
        self.entry = ttk.Entry(self.frame)
        self.enter = ttk.Button(self.frame, text="Find Urls")
        self.list = Listbox(self.frame, height=15)
        self.entry.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.enter.grid(row=0, column=1, sticky=E, padx=5, pady=5)
        self.list.grid(row=1, columnspan=2, sticky=W+E+N+S, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.grid(column=2, row=1, sticky=N+S)
        self.list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.list.yview)

        self.frame.pack(fill=BOTH)
        self.populate_list()

    def populate_list(self):
        for num in range(30):
            self.list.insert(END, num)

if __name__ == '__main__':
    root = Tk()
    app = MainWindow(root)
    root.mainloop()