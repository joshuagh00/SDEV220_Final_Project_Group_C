# settings.py
# 12/11/2023  MD Atkins
# item descriptions, for inventory & catalog

inventory_db = 'inventory.db' # name of sql database file

descriptions = \
{ # dictionary of lists, each is [description, imagefile]
    "M1": ["GT4 turbine blade", r".\images\turbine_blade.png"],
    "M2": ["FK2 fastener kit", r".\images\fasteners.png"],
    "M3": ["R3 rod", r".\images\R3rod.png"],
    "M4": ["T24 Tire ", r".\images\T24tire.png"],
    "M5": ["T8 Tire ", r".\images\T8tire.png"],
    "M6": ["W7 wheel", r".\images\W7wheel.png"],
    "M7": ["S5 strut", r".\images\S5strut.png"],
    "M8": ["A3 aileron", r".\images\A3aileron.png"],
    "M9": ["P3 prop", r".\images\P3prop.png"],
    "M10": ["P4 prop", r".\images\P4prop.png"],
    "M11": ["P5 prop", r".\images\P5prop.png"],
    "M12": ["R1 rudder", r".\images\R1rudder.png"],
    "M13": ["F2 flap", r".\images\F2flap.png"]
#    None: ["F2 flap", r".\images\nothing.png"]
}