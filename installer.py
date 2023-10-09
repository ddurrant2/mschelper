
import os
import subprocess
import json
from time import sleep

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "init.json")) as init_json: 
        init = json.load(init_json)
    subprocess.run("pip install --upgrade pip")
    result = subprocess.run(f'pip install -r requirements.txt', shell=True)
    sleep(5)
    result = subprocess.run(
        f'pyinstaller main.py -n mschelper-{init["version"]}.exe -F --windowed --icon="images\myicon.ico" --add-data "images\squarelogo.gif;." --add-data "commands.json;." --add-data "init.json;." --add-data "images\clipboard.png;."', 
        shell=True)