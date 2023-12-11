# settings.py
# 12/11/2023  MD Atkins
# item descriptions, for inventory & catalog

inventory_db = 'inventory.db' # name of sql database file

descriptions = \
{ # dictionary of lists, each is [description, imagefile]
    "GT4": ["GT4xx turbine blade", r".\images\turbine_blade.png"],
    "FK2": ["FK2y fastener kit", r".\images\fasteners.png"],
    "FK3": ["FK3x fastener kit", r".\images\fasteners.png"],
    "R3": ["R3 rod", r".\images\R3rod.png"],
    "T24": ["T24 Tire ", r".\images\T24tire.png"],
    "T8": ["T8 Tire ", r".\images\T8tire.png"],
    "W7": ["W7 wheel", r".\images\W7wheel.png"],
    "S5": ["S5 strut", r".\images\S5strut.png"],
    "A3": ["A3 aileron", r".\images\A3aileron.png"],
    "P3": ["P3 prop", r".\images\P3prop.png"],
    "P4": ["P4 prop", r".\images\P4prop.png"],
    "P5": ["P5 prop", r".\images\P5prop.png"],
    "P51": ["P51 prop", r".\images\P5prop.png"],
    "R1x": ["R1 rudder", r".\images\R1rudder.png"],
    "F2": ["F2 flap", r".\images\F2flap.png"]
#    None: ["F2 flap", r".\images\nothing.png"]
}