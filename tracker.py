# tracker.py
import sqlite3
import tkinter as tk

class AircraftPartsTracker:
    def __init__(self, inventory_listbox):
        self.conn = sqlite3.connect("aircraft_parts.db")
        self.create_table()

        self.current_part_id = 1
        self.inventory_listbox = inventory_listbox

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

    def receive_part(self, part_info):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO parts (part_number, serial_number, description, condition, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', part_info)
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

        # Clear the existing items in the listbox
        self.inventory_listbox.delete(0, tk.END)

        # Insert new items into the listbox
        for part in parts:
            self.inventory_listbox.insert(tk.END, f"{part[0]} - {part[1]} - {part[2]} - {part[3]} - {part[4]} - {part[5]}")
