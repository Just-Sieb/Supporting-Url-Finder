'''
Supporting Url Finder is opensource tool for finding what domains a site uses to host background content.

This tool is maintain by Justin Siebert and is licensed under the MIT License
'''

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from linkanalyzer import LinkFinder
from threadmanager import ProcessManager
import threading
import time
#import yappi
import logging

DEBUG = False
VERSION = "1.0.0"

if DEBUG:
    logging.basicConfig(filename="url.log", level=logging.INFO, filemode='w', format='%(levelname)s: %(asctime)s - %(message)s')
else:
    logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(asctime)s - %(message)s')



class MainWindow(ttk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.title(string="URL Finder")
        self.master.minsize(width=250, height=300)
        self.master.maxsize(width=300, height=300)

        self.show_all = BooleanVar()
        self.file = Menu(self.master, tearoff=False)
        self.file.add_command(label="About", command=self.display_about)
        self.file.add_command(label="Exit", command=self.master.quit)
        self.edit = Menu(self.master, tearoff=False)
        self.edit.add_checkbutton(label="Show All", variable=self.show_all, command=self.update_list)
        
        self.menubar = Menu(self.master)
        self.menubar.add_cascade(label="File", menu=self.file)
        self.menubar.add_cascade(label="Edit", menu=self.edit)

        self.master.config(menu=self.menubar)

        self.url = StringVar()
        self.url_analyzer = None
        self.list_of_urls = []
        self.url_dict = dict()

        self.frame = ttk.Frame(self.master)
        self.entry = ttk.Entry(self.frame, textvariable=self.url)
        self.entry.bind('<Return>', self.on_enter)
        self.enter = ttk.Button(self.frame, text="Find Urls", command=self.on_click)
        self.list = Listbox(self.frame, height=15)
        self.entry.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.enter.grid(row=0, column=1, sticky=E, padx=5, pady=5)
        self.list.grid(row=1, columnspan=2, sticky=W+E+N+S, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.grid(column=2, row=1, sticky=N+S)
        self.list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.list.yview)

        self.frame.pack(fill=BOTH)

    def populate_list(self, url_percentage):
        del self.list_of_urls[:]
        for url, percentage in sorted(url_percentage.items(), key=lambda x: x[1]):
            if self.show_all.get() is True:
                row = str(round(percentage)) + ": " + url
                self.list_of_urls.append(row)
            else:
                if percentage >= 1:
                    row = str(round(percentage)) + ": " + url
                    self.list_of_urls.append(row)

        for row in self.list_of_urls:
            self.list.insert(0, row)

    def on_click(self):
        self.list.delete(0, END)
        self.enter.config(text="Running")
        url = self.url.get()
        t = threading.Thread(target=self.run_scan, args=(url,))
        t.start()


    def run_scan(self, url):
        pm = ProcessManager(url)
        pm.start()
        count = 0
        while pm.continue_scanning:
            time.sleep(1)
            count += 1
            if count > 20:
                logging.info("Reached max timeout")
                pm.analyze_potential_urls()
                break

        self.url_dict = pm.url_percentage
        self.populate_list(pm.url_percentage)
        self.enter.config(text="Find Urls")


    def on_enter(self, event):
        self.on_click()


    def update_list(self):
        self.list.delete(0, END)
        self.populate_list(self.url_dict)


    def display_about(self):
        about = '''
                Supporting Url Finder
                Version: ''' + VERSION
        messagebox.showinfo("About", about)
        



if __name__ == '__main__':
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
