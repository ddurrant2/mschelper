"""
SOFIA - Support Over File Integrity Assurance
By Dillon Durrant
This Python Tkinter tool automates daily tasks performed by our File Integrity Assurance team.
Build from output folder: pyinstaller ..\sofia_test\main.py -n sofia-0.3.5.exe -F --windowed --icon="..\sofia_test\myicon.ico" --add-data "..\sofia_test\squarelogo.gif;."
"""
from gui import GUI 
import json
import os



if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "commands.json")) as json_file: #'C:\\USers\\ddurrant\\OneDrive - Fortress Information Security\\Documents\\Python Scripts\\SOFIA\\testjson.json') as json_file:
        data = json.load(json_file)
        newgui = GUI(data)
