# main.py
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

    # Create a ttk.Treeview instead of a Listbox
    columns = ("Part ID", "Part Number", "Serial Number", "Description", "Condition", "Quantity")
    inventory_treeview = ttk.Treeview(root, columns=columns, show="headings")

    # Set column headings
    for col in columns:
        inventory_treeview.heading(col, text=col, anchor="center")#center header text

    # Add the Treeview to the grid
    inventory_treeview.grid(row=1000, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    
    # Add a horizontal scrollbar
    horizontal_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=inventory_treeview.xview)
    horizontal_scrollbar.grid(row=1001, column=0, columnspan=2, sticky="ew")

    inventory_treeview.config(xscrollcommand=horizontal_scrollbar.set)

    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(root, command=inventory_treeview.yview)
    scrollbar.grid(row=1000, column=2, sticky="nsew")

    inventory_treeview.config(yscrollcommand=scrollbar.set)

    tracker = AircraftPartsTracker(inventory_treeview)
    gui = AircraftPartsGUI(root, tracker)

    root.mainloop()

