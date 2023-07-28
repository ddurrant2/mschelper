"""
SOFIA - Support Over File Integrity Assurance
By Dillon Durrant
This Python Tkinter tool automates daily tasks performed by our File Integrity Assurance team.
Build to .exe: pyinstaller main.py -n sofia.exe -F --windowed --add-data "squarelogo.gif;."
squarelogo.gif must be in same directory as sofia.exe
"""
from gui import GUI 

if __name__ == "__main__":
    newgui = GUI()
