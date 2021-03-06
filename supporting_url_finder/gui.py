'''
Supporting Url Finder is opensource tool for finding what domains a site uses to host background content.

This tool is maintain by Justin Siebert and is licensed under the MIT License
'''

from tkinter import Menu, BooleanVar, StringVar, sys, Tk, W, E, N, S, BOTH
from tkinter import messagebox
from tkinter import ttk
from linkanalyzer import LinkFinder
from threadmanager import ProcessManager
import threading
import time
from os import path
import logging
import platform

DEBUG = False

VERSION_MAJOR = 1
VERSION_MINOR = 1
VERSION_BUILD = 0

VERSION = "%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)


if DEBUG:
    logging.basicConfig(filename="url.log", level=logging.INFO, filemode='w', format='%(levelname)s: %(asctime)s - %(message)s')
else:
    logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(asctime)s - %(message)s')


# This is for loading the icon using the single file build process
if platform.system() == 'Windows':
    if hasattr(sys, '_MEIPASS'):
        ico_path = os.path.join(sys._MEIPASS, "url.ico")
    else:
        ico_path = path.join(path.abspath(path.join(path.dirname(__file__), '..')), "url.ico")



class MainWindow(ttk.Frame):
    def __init__(self, master):

        # Variables
        self.url = StringVar()
        self.url_analyzer = None
        self.list_of_urls = []
        self.url_dict = dict()

        # Main Window
        self.master = master
        self.master.iconbitmap(default=ico_path)
        self.master.title(string="URL Finder")
        self.master.minsize(width=300, height=375)
        self.master.maxsize(width=800, height=375)

        # Top Menu
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

        # Right-click menu for entry widget
        self.right_click_entry = Menu(self.master, tearoff=False)
        self.right_click_entry.add_command(label="Copy", command=self.copy_from_entry)
        self.right_click_entry.add_command(label="Paste", command=self.paste_to_entry)

        # Right-click menu for treeview
        self.right_click = Menu(self.master, tearoff=False)
        self.right_click.add_command(label="Copy", command=self.get_selected_url)

        # Frame containing text box and enter button
        self.top_frame = ttk.Frame(self.master)
        self.top_frame.columnconfigure(0, minsize=200, weight=10)
        self.top_frame.columnconfigure(1, minsize=100, weight=1)

        # Frame containing urls and scrollbar
        self.bottom_frame = ttk.Frame(self.master)
        self.bottom_frame.columnconfigure(0, minsize=260, weight=1000)
        self.bottom_frame.columnconfigure(1, minsize=25, weight=1)

        # Url entry box and enter button
        self.entry = ttk.Entry(self.top_frame, textvariable=self.url)
        self.entry.bind('<Return>', self.on_enter)
        self.entry.bind('<Button-3>', self.entry_popup)
        self.enter = ttk.Button(self.top_frame, text="Find Urls", command=self.on_click)

        self.entry.grid(row=0, column=0, sticky=W+E, padx=5, pady=5)
        self.enter.grid(row=0, column=1, sticky=W+E, padx=5, pady=5)

        # Url list treeview
        self.list = ttk.Treeview(self.bottom_frame, height=15, columns=['percentage', 'domain'])
        self.list['show'] = 'headings'
        self.list.column('#0', width=0)
        self.list.column('percentage', width=30, minwidth=30, stretch=False)
        self.list.column('domain', width=250, minwidth=200, stretch=False)

        self.list.heading('percentage', text="%")
        self.list.heading('domain', text='Domain')

        self.list.bind('<Control-c>', self.ctrl_c)
        self.list.bind('<Button-3>', self.treeview_popup)

        self.list.grid(row=1, column=0, sticky=W+E+N+S, padx=5, pady=5)

        # Scrollbar widget
        self.scrollbar = ttk.Scrollbar(self.bottom_frame)
        self.scrollbar.grid(column=1, row=1, sticky=N+S+E+W)
        self.list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.list.yview)

        self.top_frame.pack(fill=BOTH)
        self.bottom_frame.pack(fill=BOTH)

    def populate_list(self, url_percentage):
        del self.list_of_urls[:]
        for url, percentage in sorted(url_percentage.items(), key=lambda x: x[1]):
            if self.show_all.get() is True:
                row = (str(round(percentage)), url)
                self.list_of_urls.append(row)
            else:
                if percentage >= 1:
                    row = (str(round(percentage)), url)
                    self.list_of_urls.append(row)

        for row in self.list_of_urls:
            self.list.insert('', 0, values=row)


    def on_click(self):
        self.list.delete(*self.list.get_children())
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
            # This is to keep the system from reaching a timeout
            if count > 20:
                logging.info("Reached max timeout")
                pm.analyze_potential_urls()
                break

        self.url_dict = pm.url_percentage
        self.populate_list(pm.url_percentage)
        self.enter.config(text="Find Urls")


    def ctrl_c(self, event):
        self.get_selected_url()


    def add_to_clipboard(self, copy):
        self.master.clipboard_clear()
        self.master.clipboard_append(copy)


    def get_from_clipboad(self):
        return self.master.clipboard_get()


    def get_selected_url(self):
        curr_item = self.list.focus()
        item_dict = self.list.item(curr_item)
        self.add_to_clipboard(item_dict['values'][1])


    def paste_to_entry(self):
        self.url.set(self.get_from_clipboad())


    def copy_from_entry(self):
        self.add_to_clipboard(self.url.get())


    def treeview_popup(self, event):
        item = self.list.identify_row(event.y) # Get Row
        self.list.selection_set(item) # Highlight Row
        self.list.focus(item) # Focus Row
        self.right_click.post(event.x_root, event.y_root) # Popup menu


    def entry_popup(self, event):
        self.right_click_entry.post(event.x_root, event.y_root)

    def on_enter(self, event):
        self.on_click()


    def update_list(self):
        self.list.delete(*self.list.get_children())
        self.populate_list(self.url_dict)


    def display_about(self):
        about = "Supporting Url Finder Version: %s" % VERSION
        messagebox.showinfo("About", about)


if __name__ == '__main__':
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
