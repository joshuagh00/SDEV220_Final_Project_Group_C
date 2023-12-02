# tkinter3.py   12/02/2023
"""
Inputs: parts (items) and user badge #s (via barcode reader emulated, not really implemented), keeping track of aircraft parts received, removed from, returned to storeroom for aircraft repairs. Parts may include new and used (removed from the aircraft)?
Classes:
1. Item
Attributes: Item unique ID (S/N?), Manufacturer, Model, Description, Supplier,  image_file_path, 
    History (list of dates, conditions, and locations)
Methods: Add_history, Get_history 
2. History
List of (date, location, status) tuples (new, used good, used bad. Location = in inventory or out in field.  Perhaps the value would be the technician’s ID or the airplane ID.)

3. Inventory (Stockroom)
Attributes: list of Items
Methods: Search_item, Get_item_data, Get_inventory, Add_item, Move_item, other TBD, Save_inventory (to file, format TBD), Load_inventory (from file)
4. Employee
Attributes: Name, employee ID #, role (storeroom worker, storeroom customer, shipping/receiving, etc), security clearance, etc..
Methods: Get_employee_data, Set_clearance, others TBD
5. GUI (using Tkinter package)	
Dialog box for stockroom person
Dialog box for customer
 “Add item” button, with entry fields for new item’s attributes, 
 “Move item” button, with entry fields for item’s attributes, 
 “Search” button, with entry fields for item’s attributes
A list displaying entire inventory, scrollable
A list displaying search results
A list displaying employees, and/or a box to type employee name
Image of the item, if a single item is selected in the item list or search results list

"""
import tkinter as tk   ## tkinter GUI package
from tkinter import messagebox
from tkinter import * 
import random
import datetime
from PIL import ImageTk, Image  # to display current part image

import json  ## for writing inventory to disk file
import os.path  ## to check for file existance

random.seed()
iLengthMax = 15
filepath = './inventory.json'

#img = []
#for i in range(1)
#    img[i] = Image.open('turbine_blade.png')

IDmax = 9999


class Item:
    def __init__(self, ID=random.randrange(IDmax), description="TBD", quantity="1", imagefile = "nothing.png"):
        self.ID = ID
        self.description = description
        self.quantity = quantity
        self.imagefile = imagefile  ## the image filedescription

    def str(self):   ## create a string with item attributes
        return '%s: description: %s, Quantity: %s' % (self.ID, self.description, self.quantity)

class Inventory:
    def __init__(self):
        self.Items = {}

    def add_Item(self, ID, description, qty, imagefile):
        if ID in self.Items:
            self.Items[ID].quantity += qty
        else:
            self.Items[ID] = Item(ID, description, qty, imagefile)

    def move_Item(self, ID, qty):
        if ID in self.Items and self.Items[ID].quantity >= qty:
            self.Items[ID].quantity -= qty  ## Fixme: move should append to history, not just subtract qty
        else:
            messagebox.showerror("Error", "Not enough quantity in stock(%s) to move %s items"  % (self.Items[ID].quantity, qty))
 
    def search_Item(self, ID):
        if ID in self.Items and self.Items[ID].quantity >= 1:
            messagebox.showerror("Foumd:  %s"  % self.Items[ID].str)
## Fixme: error message displays on app initialization, but why??
# #        else:
#            messagebox.showerror("Not foumd:  Item with ID: %s"  % ID)


## Fixme: does not work: dictionary with Item object as entry can't be written as json
    def save(self, filename):  ## write inventory to disk as json
        with open(filename, 'w') as savefile: 
 #           for item in self.Items:
            savefile.write(json.dumps(self.Items))
        print("Inventory saved to %s" % filename)

    def load(self, filename):  ## read inventory from disk  json text file
        with open(filename, 'r') as rfile: 
            self.Items = json.load(rfile)
        print("Inventory read from %s" % filename)

class GUI(tk.Tk):
    def __init__(self, inventory):
        tk.Tk.__init__(self)
        self.inventory = inventory
        self.title("Inventory Management System")

        self.Item_ID_label = tk.Label(self, text="Item ID")
        self.Item_ID_label.place(x=50,y=600)
        self.Item_ID_label.pack(side = LEFT)
        self.Item_ID_entry = tk.Entry(self)
        self.Item_ID_entry.pack(side = LEFT)
        self.Item_ID_entry.insert(0, "0")

        self.Item_description_label = tk.Label(self, text=" Description")
        self.Item_description_label.pack(side = LEFT)
        self.Item_description_entry = tk.Entry(self)
        self.Item_description_entry.pack(side = LEFT)
        self.Item_description_entry.insert(0, " description")

        self.Item_quantity_label = tk.Label(self, text="Quantity")
        self.Item_quantity_label.pack(side = LEFT)
        self.Item_quantity_entry = tk.Entry(self)
        self.Item_quantity_entry.pack(side = LEFT)
        self.Item_quantity_entry.insert(0, " 1")

        self.add_button = tk.Button(self, text="Add Item", command=self.add_Item)
        self.add_button.place(x=50,y=500)

        self.move_button = tk.Button(self, text="Move Item", command=self.move_Item)
        self.move_button.place(x=150,y=500)

        self.search_button = tk.Button(self, text="Search", command=self.search_Item(self.Item_ID_entry))
        self.search_button.place(x=250,y=500)

    def add_Item(self):
        ID = self.Item_ID_entry.get()
        description = self.Item_description_entry.get()
        quantity = int(self.Item_quantity_entry.get())
        imagefile = "nothing.png"
        self.inventory.add_Item(ID, description, quantity, imagefile)

    def move_Item(self):
        ID = self.Item_ID_entry.get()
        quantity = int(self.Item_quantity_entry.get())
        self.inventory.move_Item(ID, quantity)

    def search_Item(self, ID):
        self.inventory.search_Item(ID)

if __name__ == "__main__":
 
    inventory = Inventory()
    if os.path.isfile(filepath):   ## read in inventory from file if one exists
        inventory.load(filepath)
    else:    # Populate bogus sample inventory
        for i in range(iLengthMax):
            inventory.add_Item(i, "Part type %s" % i, i+1,"turbine_blade.png")
 #      inventory.save(filepath)

    app = GUI(inventory)
    app.geometry('800x800')
    app.configure(background='#F0F0F0')
    app.title('Inventory Management System')

    # Current inventory listbox
    InventList=Listbox(app, bg='#F0F8FF', font=('arial', 12, 'normal'), width=0, height=0)
    InventList.place(x=12, y=45)
    Label(app, text='Inventory', bg='#F0F0F0', font=('arial', 12, 'normal')).place(x=35, y=20)
    for i in inventory.Items:
        InventList.insert(END, inventory.Items[i].str())
 #   while(1):
 #       for i in inventory.Items:
 #           InventList.insert(END, inventory.Items[i].str())
        # display part image
    curr_ID = int(app.Item_ID_entry.get()) ## 0  ## Kludge, fixme
    img = Image.open(inventory.Items[curr_ID].imagefile)
    tk_img = ImageTk.PhotoImage(img)
    image_label = tk.Label(app, image=tk_img)
    image_label.place(x=550,y=30)
    app.mainloop()
 #  app.update_idletasks()
 #  app.update()
        
 #   inventory.save(filepath)  ##fixme: make the save / load functions work