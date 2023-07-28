"""
SOFIA - Support Over File Integrity Assurance
By Dillon Durrant
This Python Tkinter tool automates daily tasks performed by our File Integrity Assurance team.
Build from output folder: pyinstaller ..\sofia_test\main.py -n sofia-0.3.5.exe -F --windowed --icon="..\sofia_test\myicon.ico" --add-data "..\sofia_test\squarelogo.gif;."
"""
from gui import GUI 

if __name__ == "__main__":
    newgui = GUI()
