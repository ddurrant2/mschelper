"""
MSC Helper (Masters in Cybersecurity)
By Dillon Durrant
This Python Tkinter tool assists in small tasks needed for assignments as part of my Masters in Cybersecurity program.
Build from output folder: pyinstaller mschelper\main.py -n mschelper-0.8.0.exe -F --windowed --icon="mschelper\myicon.ico" --add-data "mschelper\squarelogo.gif;." --add-data "mschelper\commands.json;."
"""
from gui import GUI 
import json
import os



if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "commands.json")) as json_file: 
        data = json.load(json_file)
        newgui = GUI(data)
