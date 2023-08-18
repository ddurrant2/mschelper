# MSC Helper

This tool is designed to assist with basic, daily tasks performed as part of my Masters program. 
See below for explanations of each panel.


## Command Builder
![image](https://github.com/ddurrant2/mschelper/assets/140553472/f4f663aa-c2c4-4416-a70b-6d25f2494c56)
This window allows the user to craft CLI commands based on allotted flags. Simply input the value for each field, click the button, and let MSC Helper generate a complete CLI command for you!

## Lower
![image](https://github.com/ddurrant2/mschelper/assets/140553472/d9cafad0-5aa9-457a-b7cf-964390e7f131)
This window allows the user to input an uppercase file hash, click the button, and output a lowercase hash to match file verification standards.

## Hash
![image](https://github.com/ddurrant2/mschelper/assets/140553472/c7337e90-61ae-434f-9f83-f44e12514419)
This window allows the user to select a file on their system, and generate file hashes for that product.

## CVE Parser
![image](https://github.com/ddurrant2/mschelper/assets/140553472/a54b4910-37ef-4fc7-bdd5-7a7751c0bd76)
This window allows the user to paste a body of text, and receive a comma-separated, redundancy-free list of CVEs for further research purposes.

## Build Instructions
(Under Construction)
Run the following command from the parent folder of the project, or other desired folder.
py -m PyInstaller mschelper\main.py -n mschelper-0.8.0.exe -F --windowed --icon="mschelper\myicon.ico" --add-data "mschelper\mylogo.gif;." --add-data "mschelper\commands.json;." --add-data "mschelper\init.json;."

