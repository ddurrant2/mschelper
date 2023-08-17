"""
Created by Dillon Durrant
This Python Tkinter app serves as a handy assistant in basic security analyst needs.
"""
from gui import GUI 
import json
import os


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "commands.json")) as comms_json: 
        comms = json.load(comms_json)
    with open(os.path.join(os.path.dirname(__file__), "init.json")) as init_json: 
        init = json.load(init_json)
    newgui = GUI(comms, init)
