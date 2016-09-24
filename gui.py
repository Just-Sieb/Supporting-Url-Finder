from tkinter import *
from tkinter import ttk
from linkanalyzer import *
import threading

class MainWindow(ttk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.title(string="URL Finder")
        self.master.minsize(width=250, height=300)
        self.master.maxsize(width=250, height=300)

        self.url = StringVar()
        self.url_analyzer = None
        self.list_of_urls = []

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

    def populate_list(self):
        self.list.delete(0, END)
        for url, percentage in self.url_analyzer.url_precentage.items():
            if percentage >= 1:
                row = str(round(percentage)) + ": " + url
                self.list_of_urls.append(row)

        for row in self.list_of_urls:
            self.list.insert(END, row)

    def on_click(self):
        self.list.delete(0, END)
        url = self.url.get()
        t = threading.Thread(target=self.run_scan, args=(url,))
        t.start()

    def on_enter(self, event):
        self.on_click()

    def run_scan(self, url):
        self.url_analyzer = LinkFinder(url, spider=1)
        self.url_analyzer.analyze()
        self.populate_list()

if __name__ == '__main__':
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
