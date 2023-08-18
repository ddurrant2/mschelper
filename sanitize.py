"""This script assists in sanitizing field inputs from gui.py"""

def VendorHash(hash):
    return hash[0].lower().strip()

def CPE(cpe):
    input = cpe[0]
    vendor = cpe[1]
    product = cpe[2]
    version = cpe[3]
    return f'cpe:2.3:a:{vendor.lower().strip().replace(" ", "_")}:{product.lower().strip().replace(" ", "_")}:{version.lower().strip().replace(" ", "_")}'