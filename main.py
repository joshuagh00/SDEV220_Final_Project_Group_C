# main.py
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins
# 12/8/23 updated M. Atkins

"""
Inputs: parts (items) (via barcode reader emulated, not really implemented), keeping track of parts received, 
removed from, returned to storeroom for aircraft repairs. Parts may include new and used (removed from the aircraft)
Classes:
1. Item
Attributes: Model #, Description, condition (new, used, good, bad) image_file_path, unique ID (SN),
    History (list of dates, conditions, and locations) (would be nice, but not implemented in this version)
    Methods: Add_history, Get_history 
2. History (would be nice, but not implemented in this version)
    List of (date, location, status) tuples (new, used good, used bad. Location = in inventory or out in field.  Perhaps the value would be the technician’s ID or the airplane ID.)

3. Inventory (Tracker)
Attributes: list of Items, kept in SQL database tabke
Methods: Add_item, Remove_item, other TBD
4. GUI (using Tkinter package)	
Dialog box
 “Add item” button, with entry fields for new item’s attributes, 
 “Remove item” button, with entry fields for item’s attributes, 
 “Search” button, with entry fields for item’s attributes
A list displaying entire inventory, scrollable
A list displaying search results
Image of the item, if a single item is selected in the item list or search results list
"""

import os
import tkinter as tk
from tkinter import ttk  # Import the ttk module (treeview)
from gui import GUI
from tracker import Tracker
from settings import descriptions

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x1000")
    
    #custom icon
    current_directory = os.getcwd()
    icon_filename= "plane.ico"
    icon_path = os.path.join(current_directory, icon_filename)

    root.iconbitmap(icon_path)

    # Create a ttk.Treeview for the inventory Listbox
    columns = ("Model #", "Description", "Condition", "Qty")
    Ilist = ttk.Treeview(root, columns=columns, show="headings")

    # Set column headings
    for col in columns:
        Ilist.heading(col, text=col, anchor="w")  # west-align header text

    # Add the Treeview to the grid
    Ilist.grid(row=1000, column=0, columnspan=3, padx=2, pady=10, sticky="nsew")
    
    # Add a horizontal scrollbar
    horizontal_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=Ilist.xview)
    horizontal_scrollbar.grid(row=1001, column=0, columnspan=2, sticky="ew")

    Ilist.config(xscrollcommand=horizontal_scrollbar.set)

    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(root, command=Ilist.yview)
    scrollbar.grid(row=1000, column=2, sticky="nsew")

    Ilist.config(yscrollcommand=scrollbar.set)
    
    tracker = Tracker(Ilist)
    gui = GUI(root, tracker)

    def on_select(event):
        # Get Ilist selected item's values
        selected = Ilist.item(Ilist.selection())
        print(selected)  # for debug
        for i in range(len(selected['values'])):  # skip field 0, which is part ID. Don't mess with last field, qty either
            gui.entry[i].delete(0, last = 30)
            gui.entry[i].insert(0, selected['values'][i])
        gui.image()  # update item image to match the model #
        gui.entry[1].delete(0, last = 30)
        descrip = descriptions[gui.entry[0].get()][0]
        gui.entry[1].insert(0, descrip)  # update to catalog description
        

    Ilist.bind('<<TreeviewSelect>>', on_select)

    root.mainloop()