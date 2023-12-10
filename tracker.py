# tracker.py
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins to add catalog database based on descriptions in settings.py.  Still need to use the database in the gui.
# 12/8/23 updated M. Atkins to add Item class, and to remove unneeded catalog database based on descriptions in settings.py.  Still need to use the catalog in the gui.
# 12/10/23 updated M. Atkins to use Item class , etc...

import sqlite3
import tkinter as tk
from tkinter import messagebox
import os

PNmax = 9999
SNmax = 9999

class Item:
    def __init__(self, mod = PNmax, desc="TBD", cond ='New?Used?', imagefile = "nothing.png", SN = SNmax):
        self.mod = mod # model number, might be alphanumeric
        self.desc = desc
        self.cond = cond
        self.imagefile = imagefile  ## the image filedescription
        # self.hist = History() class list of dates, conditions, locations Would be nice, but not implemented
        self.SN = SN  #serial # might be alphanumeric.  Unused right now  

    def str(self):   ## create a string with item attributes
        return 'model #: %s    description: %s, image: %s,  S/N: %s' % (self.mod, self.desc, self.imagefile, self.SN)
    
#class Catalog:  # superfluous
#    def __init__(self, descriptions = {}):
#        self.data = descriptions   
  

class Tracker:
    def __init__(self, Ilist=None, Clist=None):  ## Ilist defined in main.py
        self.conn = sqlite3.connect("parts.db")
        
        self.create_table()
        """
        if not os.path.isfile("catalog.db"): ## no sql catalog db yet
            self.create_ccat()
        else:
            self.ccat = sqlite3.connect("catalog.db")
        self.Clist = Clist  # catalog list
        """
        
        self.current_model = 1
        self.Ilist = Ilist  # inventory list, Ilist defined in main.py
        self.Clist = Clist  # inventory list, Ilist defined in main.py
        

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parts (
                model TEXT PRIMARY KEY,
                description TEXT,
                condition TEXT,
                qty INTEGER
            )
        ''')
        self.conn.commit()

    """
    def search(self, it):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM parts WHERE model = ?', it.mod)
        it = cursor.fetchall()
        fill_entries(it)
    """        
    def receive_part(self, it, quantity):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO parts (model, description, condition, qty)
            VALUES (?, ?, ?, ?)
               ON CONFLICT(model) DO UPDATE SET description = ?, condition = ?, qty = qty + ? ''', \
                (it.mod, it.desc, it.cond, quantity, it.desc, it.cond, quantity))
        self.conn.commit()


    def checkout_part(self, mod, quantity):
        quant = int(quantity)
        cursor = self.conn.cursor()
        cursor.execute('SELECT qty FROM parts WHERE model = ?', ([mod]))
        existing_qty = cursor.fetchone()  ## returns a tuple
        if (existing_qty):
            if (existing_qty[0] >= quant):
                cursor.execute('''UPDATE parts SET qty = qty - ?
                    WHERE model = ?  ''', (quant, mod))
                self.conn.commit()
        else:
            messagebox.showwarning("Checkout part", "Insufficient inventory (%s in stock)"% existing_qty)

    def update_inventory_display(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM parts')
        parts = cursor.fetchall()

        # Clear the existing items in the Treeview
        for item in self.Ilist.get_children():
            self.Ilist.delete(item)

        # Insert new items into the Treeview
        for part in parts:
            self.Ilist.insert("", "end", values=part)