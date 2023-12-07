# main.py
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins

import os
import tkinter as tk
from tkinter import ttk  # Import the ttk module (treeview)
from gui import AircraftPartsGUI
from tracker import AircraftPartsTracker

if __name__ == "__main__":
    root = tk.Tk()
    
    #custom icon
    current_directory = os.getcwd()
    icon_filename= "plane.ico"
    icon_path = os.path.join(current_directory, icon_filename)

    root.iconbitmap(icon_path)

    # Create a ttk.Treeview for the inveentory Listbox
    columns = ("Part Unique ID", "Part model #", "Serial #", "Description", "Condition", "Qty")
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
    

    tracker = AircraftPartsTracker(Ilist)
    gui = AircraftPartsGUI(root, tracker)

    def on_select(event):
        # Get Ilist selected item's values
        selected = Ilist.item(Ilist.selection())
        print(selected)
        for i in range(1, len(selected)):  # skip field 0, which is part ID. Don't mess with last field, qty either
            gui.entry[i-1].delete(0, last = 30)
            gui.entry[i-1].insert(0, selected['values'][i])

    Ilist.bind('<<TreeviewSelect>>', on_select)

    root.mainloop()
