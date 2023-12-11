# main.py
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins
# 12/8/23 updated M. Atkins
# 12/9/23 updated M. Atkins
# 12/10/23 updated M. Atkins


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
Methods: Add_item, Remove_item,
4. GUI (using Tkinter package)	
Dialog box
 “Add item” button, with entry fields for new item’s attributes, 
 “Remove item” button, with entry fields for item’s attributes, 
 “Search” button, with entry fields for item’s attributes
A list displaying entire inventory, scrollable
A list displaying catalog (descriptions), which is a dictionary defined in the settings.py file
Image of the item listed in the entry box(es) and/or selected in catalog or inventory
"""

import os
import tkinter as tk
from tkinter import ttk  # Import the ttk module (treeview)
# from gui import GUI
from tracker import Tracker
from settings import *

listheight = 14

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x700") # has no effect, due to the grid 
 #   root.grid(baseWidth=6, baseHeight=5, widthInc=1, heightInc=1)  #doesn't really work, too large

    #custom icon
    current_directory = os.getcwd()
    icon_filename= "plane.ico"
    icon_path = os.path.join(current_directory, icon_filename)
    root.iconbitmap(icon_path)

    # Function to sort a Treeview by column
    def sort_treeview(tree, col, descending):
        data = [(tree.set(item, col), item) for item in tree.get_children('')]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
          tree.move(item, '', index)
        tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))

  #########################################################################
    labelrow = 0; treerow = 1  # locations
    # Create Catalog Listbox, a ttk.Treeview 
    label_Clist = tk.Label(text="Catalog", font=("Arial", 16))
    label_Clist.grid(row=labelrow, column=0, padx=10, pady=1, sticky="ws")
 
    columns = ("Model #", "Description")
    Clist = ttk.Treeview(root, columns=columns, show="headings", height=listheight)
    # Set column headings
    for col in columns:
        Clist.heading(col, text=col, anchor="w", command=lambda c=col: sort_treeview(Clist, c, False))  # west-align header text
    Clist.column(0, width=90)
    Clist.column(1, width=200)  # description columun wide
 
    # Add the Treeview to the grid
    Clist.grid(row=treerow, column=0, columnspan=2, rowspan=3, padx=10, pady=10, sticky="nw")

    # Add a vertical scrollbar
    scrollbarC = tk.Scrollbar(root, command=Clist.yview)
    scrollbarC.grid(row=treerow, column=2, sticky="nsw")
    Clist.config(yscrollcommand=scrollbarC.set)

    for key in descriptions:  ## convert dict entries to tuple to insert in treeview
        Clist.insert('', 'end', values=(key, descriptions[key][0]))
    
    ##########################################################################
    # Create inventory Listbox, a ttk.Treeview 
    label_Ilist = tk.Label(text="Inventory", font=("Arial", 16))
    label_Ilist.grid(row=labelrow, column=3, padx=10, pady=1, sticky="ws")
  
    columns = ("Model #", "Description", "Condition", "Quantity", "Updated")
    Ilist = ttk.Treeview(root, columns=columns, show="headings", height=listheight)

    # Set column headings
    for col in columns:
        Ilist.heading(col, text=col, anchor="w", command=lambda c=col: sort_treeview(Ilist, c, False))  # west-align header text
        Ilist.column(col, width=80)
    Ilist.column(1, width=150)  # description columun wide
    Ilist.column(4, width=150)  # description columun wide
     
    # Add the Treeview to the grid
    Ilist.grid(row=treerow, column=3, columnspan=4, padx=10, pady=10, sticky="nw")

    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(root, command=Ilist.yview)
    scrollbar.grid(row=treerow, column=7, sticky="nesw")
    Ilist.config(yscrollcommand=scrollbar.set)

    # Could Add a horizontal scrollbar
    # horizontal_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=Ilist.xview)
    # horizontal_scrollbar.grid(row=8, column=0, columnspan=4, sticky="ew")
    # Ilist.config(xscrollcommand=horizontal_scrollbar.set)

    tracker = Tracker(Ilist, Clist)

    from gui import GUI
    gui1 = GUI(root, tracker, Ilist, Clist)
   ############### Functions to populate entries from treeview selections ######
    
    def on_select_I(event):
        #for i in Clist.selection(): Clist.selection_remove(i)  # clear any selections in other list 
        # Get treeview(s) selected item's values
        selected = Ilist.item(Ilist.selection())
    #    print("inventory selected:", selected)  # for debug
        
        gui1.fill_entries(selected['values'])
        gui1.image()  # update item image to match the model #
  
         # update description field to catalog description
        if gui1.entry[0].get() in descriptions:  # avoid KeyError on dictionary
            descrip = descriptions[gui1.entry[0].get()][0]
            gui1.entry[1].delete(0, last = 30) 
            gui1.entry[1].insert(0, descrip)  # update to catalog description

    def on_select_C(event):
        #for i in Ilist.selection(): Ilist.selection_remove(i)  # clear any selections in other list
        # Get treeview(s) selected item's values
        selected = Clist.item(Clist.selection())
      #  print("Catalog selected:", selected)  # for debug
        gui1.fill_entries(selected['values'])
        gui1.image()  # update item image to match the model #
        
         # update description field to catalog description
        if gui1.entry[0].get() in descriptions:  # avoid KeyError on dictionary
            descrip = descriptions[gui1.entry[0].get()][0]
            gui1.entry[1].delete(0, last = 30) 
            gui1.entry[1].insert(0, descrip)  # update to catalog description
            gui1.entry[3].delete(0, last = 30)  # remove quantity
        
    Ilist.bind('<<TreeviewSelect>>', on_select_I)
    Clist.bind('<<TreeviewSelect>>', on_select_C)

    gui1.time_update()
    root.mainloop()