# gui.py  
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins

import tkinter as tk
# from tkinter import simpledialog
from tracker import AircraftPartsTracker

class AircraftPartsGUI:
    def __init__(self, master, tracker):
        self.master = master
        self.master.title("Aircraft Parts Tracker")
        self.master.geometry("1000x1000")

        self.tracker = tracker

        labels = ["Part Model #", "Serial #", "Description", "Condition", "Quantity"]
        self.entry = [tk.Entry(master)] # length 1 list of entry boxes

        for row, label_text in enumerate(labels):
            label = tk.Label(master, text=label_text)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

            self.entry.append (tk.Entry(master))
            self.entry[row].grid(row=row, column=1, padx=10, pady=5, sticky="w")

        # Buttons
        receive_button = tk.Button(master, text="Receive Part", command=self.receive_part)
        receive_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

        checkout_button = tk.Button(master, text="Checkout Part", command=self.checkout_part)
        checkout_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

        # Update inventory display initially
        self.tracker.update_inventory_display()

        # Center the GUI
        for i in range(len(labels) + 3):
            master.grid_rowconfigure(i, weight=1)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        
        self.part_info =[]
        for x in self.entry:
            self.part_info.append(x.get())


    def receive_part(self):
        self.part_info =[]
        for x in self.entry:
            self.part_info.append(x.get())
        self.tracker.receive_part(self.part_info)
        self.tracker.update_inventory_display()

    def checkout_part(self):
        self.part_info =[]
        for x in self.entry:
            self.part_info.append(x.get())
        #part_number = simpledialog.askstring("Checkout Part", "Enter Part Number:")
        #if part_number:
        #    quantity = simpledialog.askinteger("Checkout Part", "Enter Quantity:")
        #    if quantity:
        self.tracker.checkout_part(self.part_info[0], self.part_info[5])
        self.tracker.update_inventory_display()

if __name__ == "__main__":
    root = tk.Tk()
    tracker = AircraftPartsTracker()
    gui = AircraftPartsGUI(root, tracker)
    root.mainloop()
