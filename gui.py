# gui.py  
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins
# 12/8/23 updated M. Atkins
# 12/9/23 updated M. Atkins
# 12/10/23 updated M. Atkins
import tkinter as tk

from PIL import ImageTk, Image  # to display current part image
from datetime import datetime  # for  TOD display label and History list (not yet implemented)

from tracker import Tracker, Item
from settings import *

class GUI:
    def __init__(self, master, tracker, Ilist, Clist):
        self.master = master
        self.master.title("Aircraft Parts Tracker")
        self.master.geometry("1000x600")
        self.Ilist = Ilist
        self.Clist = Clist
        self.tracker = tracker

        now = datetime.now()
        date_time = now.strftime(" %H:%M:%S  %m/%d/%Y") # Format the date and time
        self.label_time = tk.Label(master, text=date_time)
        self.label_time.grid(row=0, column=2, padx=1, pady=5, sticky="w")

        labels = ["Model #", "Description", "Condition", "Quantity"]  # "Serial #",
        self.entry = [] # length 0 list of entry boxes

        for row, label_text in enumerate(labels):
            label = tk.Label(master, text=label_text)
            label.grid(row=row, column=0, padx=1, pady=5, sticky="e")

            self.entry.append (tk.Entry(master))
            self.entry[row].grid(row=row, column=1, padx=1, pady=5, sticky="w")

        # Buttons
        button_Search = tk.Button(master, text="Search", command=self.search)
        button_Search.grid(row=1, column=2, padx=1, pady=5) #, columnspan=1, pady=1)

        button_Add = tk.Button(master, text="Receive item", command=self.receive_part)
        button_Add.grid(row=2, column=2, padx=1, pady=5) #, columnspan=1, pady=1)

        checkout_button = tk.Button(master, text="Checkout item", command=self.checkout_part)
        checkout_button.grid(row=3, column=2, padx=1, pady=5) #, columnspan=1, pady=1)

        # Update inventory display initially
        self.tracker.update_inventory_display()

        master.grid_columnconfigure(0, weight=0)
        master.grid_columnconfigure(1, weight=0)
            
        self.get_it()

    def get_it(self):  ## get item data from entry boxes
        self.it = Item(self.entry[0].get(),self.entry[1].get(),self.entry[2].get(), None, None) 
        self.quantity = self.entry[3].get()

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

    def time_update(self):
        now = datetime.now()
        date_time = now.strftime(" %H:%M:%S     %m/%d/%Y") # Format the date and time
        self.label_time.config(text=date_time)
        self.master.after(100, self.time_update)   # Schedule to run evry 100ms 

## Button methods:
    def search(self):
        for i in self.Ilist.selection(): self.Ilist.selection_remove(i)  # clear any selections
        for i in self.Clist.selection(): self.Clist.selection_remove(i)
       
        query = self.entry[0].get()  ## just searching model #
        if query != '':
            selections = []
            for child in self.Ilist.get_children():  ## look first in the inventory
                if query in self.Ilist.item(child)['values']:   # compare strings
                   # print(self.Ilist.item(child)['values'])  # for debug
                    selections.append(child)
                    self.Ilist.selection_set(selections)
                    self.image()
                    return
                else: 
                    for child in self.Clist.get_children():
                        if query in self.Clist.item(child)['values']:  
                            selections.append(child)
                            self.Clist.selection_set(selections)
                            self.image()
                            return
   
    def receive_part(self):
        self.get_it()
        self.image()  # show picture for whatever is in Model # entry
        if (not self.quantity.isnumeric()):  ## no quantity or nonumber 
            tk.messagebox.showwarning("Receive item", "Invalid or missing quantity to receive")
        else:    
            self.tracker.receive_part(self.it, self.quantity)
            self.tracker.update_inventory_display()    

    def checkout_part(self):
        self.get_it()
        self.image()  # show picture for whatever is in Model # entry
        if (not self.quantity.isnumeric()):  ## no quantity or nonumber 
            tk.messagebox.showwarning("Checkout item", "Invalid or missing quantity")
        else:    
            self.tracker.checkout_part(self.it.mod, self.quantity)
            self.tracker.update_inventory_display()