# tooltips.py
# MD Atkins 12/12/2023
# adapted from Edge copilot search
# Usage:
#  createToolTip(btn, "This is a button")
#  createToolTip(entry, "This is an entry box")

import tkinter as tk

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text): #   "Display text in a tooltip window"
        if self.tip_window or not tip_text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 60
        y += self.widget.winfo_rooty() + 10
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=tip_text, background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def show(event):
        toolTip.show_tip(text)
    def hide(event):
        toolTip.hide_tip()
    widget.bind('<Enter>', show)
    widget.bind('<Leave>', hide)
    widget.bind('<FocusIn>', hide)