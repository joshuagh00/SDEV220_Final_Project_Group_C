# main.py
import tkinter as tk
from gui import AircraftPartsGUI
from tracker import AircraftPartsTracker

if __name__ == "__main__":
    root = tk.Tk()

    inventory_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=10)
    inventory_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    tracker = AircraftPartsTracker(inventory_listbox)
    gui = AircraftPartsGUI(root, tracker)

    root.mainloop()

