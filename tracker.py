# tracker.py
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins to add catalog database based on descriptions in settings.py.  Still need to use the database in the gui.
# 12/8/23 updated M. Atkins to add Item class, and to remove unneeded catalog database based on descriptions in settings.py.  Still need to use the database in the gui.

import sqlite3
import tkinter as tk
import os
from settings import descriptions
PNmax = 9999
SNmax = 9999

class Item:
    def __init__(self, model = PNmax, description="TBD", condition ='New?Used?', imagefile = "nothing.png", SN = SNmax):
        self.model = model # , might be alphanumeric
        self.description = description
        self.condition = condition
        self.imagefile = imagefile  ## the image filedescription
        # self.hist = History()  Would be nice, but not implemented
        self.SN = SN  #serial # , might be alphanumeric    

    def str(self):   ## create a string with item attributes
        return 'model #: %s    description: %s, image: %s,  S/N: %s' % (self.model, self.description, self.imagefile, self.SN)
    


class Tracker:
    def __init__(self, Ilist=None): # unneeded:   , Clist=None):
        self.conn = sqlite3.connect("parts.db")
        
        self.create_table()
        """
        if not os.path.isfile("catalog.db"): ## no catalog yet
            self.create_ccat()
        else:
            self.ccat = sqlite3.connect("catalog.db")
        self.Clist = Clist  # catalog list
        """
        
        self.current_model = 1
        self.Ilist = Ilist  # inventory list
        

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

    def receive_part(self, part_info):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO parts (model, description, condition, qty)
            VALUES (?, ?, ?, ?)
               ON CONFLICT(model) DO UPDATE SET qty = qty + ? ''', \
                (part_info[0], part_info[1], part_info[2], part_info[3], part_info[3]))
        self.conn.commit()

    def checkout_part(self, mod, quantity):
        quant = int(quantity)
        cursor = self.conn.cursor()
        cursor.execute('SELECT qty FROM parts WHERE model = ?', ([mod]))
        existing_qty = cursor.fetchone()  ## returns a tuple
        if (existing_qty[0] >= quant):
            cursor.execute('''UPDATE parts SET qty = qty - ?
                WHERE model = ?  ''', (quant, mod))
            self.conn.commit()
        else:
            tk.messagebox.showwarning(title="Checkout part", message="Insufficient quantity (str((existing_qty))")

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
    """

    def create_ccat(self):  ## make catalog of parts and images
            self.ccat = sqlite3.connect("catalog.db")
            cursor = self.ccat.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS catalog (
                 model TEXT PRIMARY KEY, 
                 description TEXT,
                 imagefile TEXT
                )
            ''')
            for i in range(len(descriptions)):
                cursor.execute('''
                    INSERT INTO catalog (model, description, imagefile)
                    VALUES (?, ?, ?)
                ''', [i, descriptions[i][0], descriptions[i][1]])
            self.ccat.commit()        

    def update_ccat_display(self):
        cursor = self.ccat.cursor()
        cursor.execute('SELECT * FROM catalog')
        cat_list = cursor.fetchall()

        # Clear the existing items in the Treeview
        for item in self.Clist.get_children():
            self.Clist.delete(item)

        # Insert new items into the Treeview
        for part in cat_list:
            self.Clist.insert("", "end", values=part)      
    """