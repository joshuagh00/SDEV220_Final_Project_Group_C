# tracker.py
# 12/7/23 D. Kolb
# 12/7/23 updated M. Atkins to add catalog database based on descriptions in settings.py.  Still need to use the database in the gui.

import sqlite3
import tkinter as tk
import os
from settings import descriptions

class AircraftPartsTracker:
    def __init__(self, Ilist=None, Clist=None):
        self.conn = sqlite3.connect("parts.db")
        
        self.create_table()
        if not os.path.isfile("catalog.db"): ## no catalog yet
            self.create_ccat()
        else:
            self.ccat = sqlite3.connect("catalog.db")
        
        self.current_part_id = 1
        self.Ilist = Ilist  # inventory list
        self.Clist = Ilist  # catalog list

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parts (
                part_id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_number TEXT,
                serial_number TEXT,
                description TEXT,
                condition TEXT,
                quantity INTEGER
            )
        ''')
        self.conn.commit()

    def create_ccat(self):  ## make catalog of parts and images
            self.ccat = sqlite3.connect("catalog.db")
            cursor = self.ccat.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS catalog (
                 part_number INTEGER PRIMARY KEY, 
                 description TEXT,
                 imagefile TEXT
                )
            ''')
            for i in range(len(descriptions)):
                cursor.execute('''
                    INSERT INTO catalog (part_number, description, imagefile)
                    VALUES (?, ?, ?)
                ''', [i, descriptions[i][0], descriptions[i][1]])
            self.ccat.commit()   
        

    def receive_part(self, part_info):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO parts (part_number, serial_number, description, condition, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', part_info[0:5])
        self.conn.commit()

    def checkout_part(self, part_number, quantity):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE parts
            SET quantity = quantity - ?
            WHERE part_number = ?
        ''', (quantity, part_number))
        self.conn.commit()

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
        
