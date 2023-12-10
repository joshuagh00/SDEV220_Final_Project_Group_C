# gui.py  
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins
# 12/8/23 updated M. Atkins
# 12/9/23 updated M. Atkins

import tkinter as tk
# from tkinter import simpledialog
from PIL import ImageTk, Image  # to display current part image

from tracker import Tracker
from settings import *

class GUI:
    def __init__(self, master, tracker, Ilist):
        self.master = master
        self.master.title("Aircraft Parts Tracker")
        self.master.geometry("1000x1000")
        self.Ilist = Ilist

        self.tracker = tracker

        labels = ["Model #", "Description", "Condition", "Quantity"]  # "Serial #",
        self.entry = [] # length 0 list of entry boxes

        for row, label_text in enumerate(labels):
            label = tk.Label(master, text=label_text)
            label.grid(row=row, column=0, padx=1, pady=5, sticky="e")

            self.entry.append (tk.Entry(master))
            self.entry[row].grid(row=row, column=1, padx=1, pady=5, sticky="w")

        # Buttons
        button_Search = tk.Button(master, text="Search", command=self.search)
        button_Search.grid(row=0, column=2, padx=1, pady=5) #, columnspan=1, pady=1)

        button_Add = tk.Button(master, text="Receive item", command=self.receive_part)
        button_Add.grid(row=1, column=2, padx=1, pady=5) #, columnspan=1, pady=1)

        checkout_button = tk.Button(master, text="Checkout item", command=self.checkout_part)
        checkout_button.grid(row=2, column=2, padx=1, pady=5) #, columnspan=1, pady=1)

        label_Ilist = tk.Label(master, text="Inventory", font=("Arial", 16))
        label_Ilist.grid(row=7, column=0, padx=10, pady=1, sticky="w")

        label_Clist = tk.Label(master, text="Catalog", font=("Arial", 16))
        label_Clist.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        # Update inventory display initially
        self.tracker.update_inventory_display()

        # Center the GUI
        #for i in range(len(labels)):
        #    master.grid_rowconfigure(i, weight=1)
        master.grid_columnconfigure(0, weight=0)
        master.grid_columnconfigure(1, weight=0)
        
        self.part_info =[]  ## part info is a list.  FIXME: Should be a class Item() instance instead
        for x in self.entry:
            self.part_info.append(x.get())
    
        #self.cata = Catalog(descriptions)

    def image(self):  ## place image corresponding to this part model #
            self.model = self.entry[0].get() 
            default_image = [r'.\images\nothing.png', r'.\images\nothing.png']  # make a list to match descriptoin format 
            image_loc = descriptions.get(self.model,default_image)[1]  # default if key not found, avoid exception
            self.img = Image.open(image_loc) 
            #self.img = self.img.resize((200, 300))   #doesn't work right, maybe because its a .png         
            self.tk_img = ImageTk.PhotoImage(self.img)
            self.image_label = tk.Label(self.master, image=self.tk_img)
            self.image_label.place(x=600,y=3)
            #self.image_label.grid(row=0, column=3, rowspan=3, columnspan=1, padx=0, pady=0, sticky="ne")
 
    def fill_entries(self, values):
        for i in range(len(values)):  
            self.entry[i].delete(0, last = 30)
            self.entry[i].insert(0, values[i])    

## Button methods:
    def search(self):
        # self.part_info =[]
        # for x in self.entry :   # get current entry box part info
        #   self.part_info.append(x.get())

        query = self.entry[0].get()  ## just searching model #
        selections = []
        for child in self.Ilist.get_children():
            if query in self.Ilist.item(child)['values']:   # compare strings
         #       print(self.Ilist.item(child)['values'])  # for debug
                selections.append(child)
        # print('search completed')
        self.Ilist.selection_set(selections)
        self.image()
        # fill_entries(part_info)
   

    def receive_part(self):
        self.part_info = []
        for x in self.entry:
            self.part_info.append(x.get())
        self.image()  # show picture for whatever is in Model # entry
        if (not self.part_info[3].isnumeric()):  ## no quantity or nonumber 
            tk.messagebox.showwarning("Receive item", "Invalid or missing quantity to receive")
        else:    
            self.tracker.receive_part(self.part_info)
            self.tracker.update_inventory_display()    

    def checkout_part(self):
        self.part_info =[]
        for x in self.entry:
            self.part_info.append(x.get())
        self.image()  # show picture for whatever is in Model # entry
        if (not self.part_info[3].isnumeric()):  ## no quantity or nonumber 
            tk.messagebox.showwarning("Checkout item", "Invalid or missing quantity")
        else:    
            self.tracker.checkout_part(self.part_info[0], self.part_info[3])
            self.tracker.update_inventory_display()