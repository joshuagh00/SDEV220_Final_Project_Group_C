# gui.py  
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins
# 12/8/23 updated M. Atkins
# 12/9/23 updated M. Atkins
# 12/10/23 updated M. Atkins
# 12/11/23 updated M. Atkins
# 12/12/23 updated M. Atkins. Tweaks to tooltips and search button messageboxes
import tkinter as tk

from PIL import ImageTk, Image  # to display current part image
from datetime import datetime  # for  TOD display label and History list (not yet implemented)

from tracker import Tracker, Item
from settings import *
from tooltips import *

class GUI:
    def __init__(self, master, tracker, Ilist, Clist):
        self.master = master
        self.master.title("Aircraft Parts Tracker")
        
        self.Ilist = Ilist
        self.Clist = Clist
        self.tracker = tracker

        offset = 7  # row offset for the widgets
        # initialize timeclock.  Could use this in the inventory table, if timestamp implemented
        now = datetime.now()
        date_time = now.strftime(" %H:%M:%S  %m/%d/%y ") # Format the date and time
        self.label_time = tk.Label(master, text=date_time, bg='yellow', bd=2, relief="raised")
        self.label_time.grid(row=offset, column=2, padx=1, pady=5, sticky="w")

        labels = ["Model", "Description", "Condition", "Quantity"]  # "Serial #",
        self.entry = [] # length 0 list of entry boxes
      

        for r, label_text in enumerate(labels):
            label = tk.Label(master, text=label_text)
            label.grid(row=offset+r, column=0, padx=1, pady=5, sticky="e")

            self.entry.append (tk.Entry(master))
            self.entry[r].grid(row=offset+r, column=1, padx=1, pady=5, sticky="w")

        # Buttons
        button_Search = tk.Button(master, text="Search", command=self.search)
        button_Search.grid(row=offset+1, column=2, padx=1, pady=5) #, columnspan=1, pady=1)

        button_Add = tk.Button(master, text="Add item", command=self.receive_part)  ##  "Add item to\n inventory"
        button_Add.grid(row=offset+2, column=2, padx=1, pady=5) #, columnspan=1, pady=1)

        button_out = tk.Button(master, text="Checkout item", command=self.checkout_part)
        button_out.grid(row=offset+3, column=2, padx=1, pady=5) #, columnspan=1, pady=1)

        # Update inventory display initially
        self.tracker.update_inventory_display()

        master.grid_columnconfigure(0, weight=0)
        master.grid_columnconfigure(1, weight=0)

        createToolTip(button_Search, "Search for Model in\n inventory, then in catalog")
        createToolTip(button_Add, "Add to inventory the quantity\n of item selected or listed")
        createToolTip(button_out, "Remove from inventory the quantity\n of item selected or listed")
        createToolTip(self.entry[0], "Enter model or select an item in Catalog\n or Inventory to populate the blanks")
        createToolTip(self.entry[1], "Enter description or select an item in Catalog\n or Inventory to populate the blanks")
        createToolTip(self.entry[3], "A positive numeral for the quantity\n to add or checkout")
           
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
            #self.image_label.place(x=600,y=370)
            self.image_label.grid(row=7, column=3, rowspan = 4, padx=0, pady=0, sticky="ne") # may expand row size to image height
 
    def fill_entries(self, values):
        for i in range(len(values)-1):  
            self.entry[i].delete(0, last = 30)
            self.entry[i].insert(0, values[i])  

    def time_update(self):
        now = datetime.now()
        date_time = now.strftime(" %H:%M:%S     %m/%d/%y ") # Format the date and time
        self.label_time.config(text=date_time)
        self.master.after(100, self.time_update)   # Schedule to run evry 100ms 

## Button methods:
    def search(self):
        for i in self.Ilist.selection(): self.Ilist.selection_remove(i)  # clear any selections
        for i in self.Clist.selection(): self.Clist.selection_remove(i)
       
        query = self.entry[0].get()  ## just searching model #
        if query == '' or query.isspace():
            tk.messagebox.showwarning("Search lists for Model", "Please supply Model")
            return
        else:
            selections = []
            children = self.Ilist.get_children()
            if len(children):  ## not an empty tuple
                for child in children:  ## look first in the inventory
                    # print(self.Ilist.item(child)['values'])  # for debug
                    if query in self.Ilist.item(child)['values']:   # compare strings                       
                        selections.append(child)
                        self.Ilist.selection_set(selections)
                        self.image()
                        return
                ## look in catalog if not in inventory
            children = self.Clist.get_children()
            if len(children):
                for child in self.Clist.get_children():
                    if query in self.Clist.item(child)['values']:  
                        selections.append(child)
                        self.Clist.selection_set(selections)
                        self.image()
                        return
        notfound = "Model %s not found but can be added\n to inventory via Add item button" % query
        tk.messagebox.showinfo("Search for model", notfound)  ## here if neither list has the model
 
    def receive_part(self):
        self.get_it()
        if (self.it.mod == '' or self.it.mod.isspace() or not self.quantity.isnumeric()):  ## no model number 
            tk.messagebox.showwarning("Add item", "Please supply Model and\n also quantity as a numeral")
        else:
            self.image()  # show picture for whatever is in Model # entry
            if (self.it.desc == '' or self.it.desc.isspace()):  ## add missing description
                for child in self.Clist.get_children():
                        if self.it.mod in self.Clist.item(child)['values']:  
                            self.Clist.selection_set(child)
                            self.it.desc =self.Clist.item(child)['values'][1]
                            self.entry[1].insert(0,self.it.desc) 
                            break
            self.tracker.receive_part(self.it, self.quantity)
            self.tracker.update_inventory_display()    

    def checkout_part(self):
        self.get_it()
        if (self.it.mod == '' or self.it.mod.isspace() or not self.quantity.isnumeric()):  ## no model number 
            tk.messagebox.showwarning("Chekout item", "Please supply Model and\n also quantity as a numeral")
        else:    
            self.image()  # show picture for whatever is in Model entry 
            self.tracker.checkout_part(self.it.mod, self.quantity)
            self.tracker.update_inventory_display()