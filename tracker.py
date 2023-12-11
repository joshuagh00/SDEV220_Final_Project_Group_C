# tracker.py
# 12/7/23 D. Kolb using sqlite database, etc.
# 12/7/23 updated M. Atkins to add catalog database based on descriptions in settings.py.  Still need to use the database in the gui.
# 12/8/23 updated M. Atkins to add Item class, and to remove unneeded catalog database based on descriptions in settings.py.  Still need to use the catalog in the gui.
# 12/10/23 updated M. Atkins to use Item class , etc...
# 12/11/23 updated M. Atkins to include time TOD of inventory list update

import sqlite3
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime  # for TOD of inventory list update
from settings import *
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
        self.conn = sqlite3.connect(inventory_db)
        
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
            CREATE TABLE IF NOT EXISTS inventory (
                model TEXT PRIMARY KEY,
                description TEXT,
                condition TEXT,
                qty INTEGER,
                time TEXT
            )
        ''')
        self.conn.commit()

    """  ## Search database function, unneeded because we just search the catalog and inventory listboxes
    def search(self, it):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM inventory WHERE model = ?', it.mod)
        it = cursor.fetchall()
        fill_entries(it)
    """        
    def receive_part(self, it, quantity):
        now = datetime.now()
        self.time = now.strftime("%H:%M:%S  %m/%d/%y") # Format the date and time
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (model, description, condition, qty, time)
            VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(model) DO UPDATE SET description = ?, condition = ?, qty = qty + ?, time=?''',
                (it.mod, it.desc, it.cond, quantity, self.time, it.desc, it.cond, quantity, self.time))
        self.conn.commit()


    def checkout_part(self, mod, quantity):
        now = datetime.now()
        self.time = now.strftime("%H:%M:%S  %m/%d/%y") # Format the date and time
        quant = int(quantity)
        cursor = self.conn.cursor()
        cursor.execute('SELECT qty FROM inventory WHERE model = ?', ([mod]))
        existing_qty = cursor.fetchone()  ## returns a tuple
        if (existing_qty != None):
            if (existing_qty[0] >= quant):
                cursor.execute('''UPDATE inventory SET qty = qty - ?, time = ?
                    WHERE model = ?  ''', (quant, self.time, mod))
                self.conn.commit()
            else:
                messagebox.showwarning("Checkout part", "Insufficient inventory (%s in stock)"% existing_qty)
        else:
                messagebox.showwarning("Checkout part", "Insufficient inventory (%s in stock)"% existing_qty)


    def update_inventory_display(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM inventory')
        inventory = cursor.fetchall()

        # Clear the existing items in the Treeview
        for item in self.Ilist.get_children():
            self.Ilist.delete(item)

        # Insert new items into the Treeview
        for part in inventory:
            self.Ilist.insert("", "end", values=part)