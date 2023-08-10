from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
import re
import webbrowser
import pathlib

version = "v0.8 Alpha"
WIN_HEIGHT = 540
WIN_WIDTH = 960
COL_MAX = 11

WINDOW_BAR = '#3F58C8'
WINDOW_BAR_TEXT = '#FFFFFF'
UPPER_NOTEBOOK_FILLER = '#95A1DB'
UPPER_TAB_INACTIVE = '#BAC6FF'
UPPER_TAB_ACTIVE = '#FFFFFF'
LOWER_NOTEBOOK_OUTLINE = '#6471A8'
ACTIVE_TAB_TEXT = '#000000'
FLAG_FILLER_TEXT = '#CACCD6'
BUILD_BUTTON_FILLER = '#BAC6FF'
BUILD_BUTTON_TEXT = '#000000'

class GUI:
    """
    The GUI class creates and maintains all Tkinter features of the app.
    """

    def __init__(self, json_file):
        #self.TestJson(json_file)
        self.json = json_file
        """Initializes and creates the Tkinter window and Notebook sections"""
        root = Tk()
        root.option_add('*tearOff', False)
        root.title("SOFIA - Support Over FIA")
        root.resizable(False, False)
        try:
            icon = PhotoImage(
                file=os.path.join(os.path.dirname(__file__), "squarelogo.gif")) #file="C:\\Users\\ddurrant\\Documents\\squarelogo.gif"
            root.iconphoto(True, icon)
        except:
            root.iconphoto(False)
        self.notebook = ttk.Notebook(root, height=WIN_HEIGHT, width=WIN_WIDTH)
        self.notebook.grid()
        self.SetupWindows(root)
        self.SetupCommandBuilder()
        self.SetupLower()
        self.SetupHash()
        self.SetupCVEParse()

        root.mainloop()

    def TestJson(self, json_file):
        for key, value in json_file.items():
            print(json_file[key]["title"])
            f'The {json_file[key]["title"]} command has the following flags:'
            for flag in json_file[key]["flags"]:
                print(f'{flag[0]}{"*" if flag[1] == True else ""}: {flag[2]}')

    def SetupWindows(self, root):
        """Initializes frames for each tab"""
        # Info footer
        self.infoFooter = ttk.Frame(root)
        # Create frames for each tab
        self.lowerFrame = ttk.Frame(self.notebook)
        self.hashFrame = ttk.Frame(self.notebook)
        self.commandBuilderFrame = ttk.Frame(self.notebook)
        self.cveBodySearchFrame = ttk.Frame(self.notebook)

        # add frames to notebook with tab names
        self.notebook.add(self.commandBuilderFrame, text="Command Builder")
        self.notebook.add(self.lowerFrame, text="Lower()")
        self.notebook.add(self.hashFrame, text="Hash a File")
        self.notebook.add(self.cveBodySearchFrame, text="CVE Body Search")

        # Add descriptions to each tab
        Label(self.lowerFrame, text="Find a Vendor Hash that's in caps? \nPaste it below to get the lower case version!", font=(
            "Helvetica", 12)).grid(pady=15, sticky='news')
        Label(self.hashFrame, text="Hash a file with ease! \nSelect your file below.", font=(
            "Helvetica", 12)).grid(pady=15, sticky='news')
        Label(self.commandBuilderFrame, text="Handy tool for crafting CLI commands!", font=(
            "Helvetica", 12)).grid(pady=15, sticky='news')
        Label(self.cveBodySearchFrame, text="Got a changelog with too many CVE's? \nPaste the whole body here and we'll give you a comma-separated list!",
              font=("Helvetica", 12)).grid(pady=15, sticky='news')
        self.infoFooter.grid()
        Label(self.infoFooter,
              text=f"Created by Dillon Durrant - {version}").grid()

    def SetupLower(self):
        """Sets up and maintains the frame for lowering a file hash"""

        # Entry field where users will put their uppercase hashes
        Label(self.lowerFrame, text="Uppercase Hash:").grid(row=1, column=0)
        self.upperText = StringVar()
        self.upper = Entry(
            self.lowerFrame, textvariable=self.upperText, width=64)
        self.upper.grid(row=3, column=0)

        # Button that carries out the .lower() method
        self.lowerButton = ttk.Button(
            self.lowerFrame, text="Go!", command=self.LowerText)
        self.lowerButton.grid(row=4, column=0, pady=10)

        # Done message says that the operation is done.
        self.done = Label(self.lowerFrame)
        self.done.grid(row=5, column=0)

        # Displays the result of the .lower() method
        Label(self.lowerFrame, text="Lowercase Hash:").grid(row=6, column=0)
        self.result = Text(self.lowerFrame, height=1)
        self.result.grid(row=7, column=0, padx=10)

    def SetupHash(self):
        """Sets up and maintains the frame for retrieving file hashes"""
        # Set up frames inside window
        self.md5Frame = ttk.Frame(self.hashFrame)
        self.md5Frame.grid(row=3, column=0)
        self.sha1Frame = ttk.Frame(self.hashFrame)
        self.sha1Frame.grid(row=4, column=0)
        self.sha256Frame = ttk.Frame(self.hashFrame)
        self.sha256Frame.grid(row=5, column=0)

        # Set up label and button for finding file
        self.hashFileName = Label(self.hashFrame, text="No file selected")
        self.hashFileName.grid(row=1, column=0)
        self.hashButton = ttk.Button(
            self.hashFrame, text="Select File", command=self.HashFile)
        self.hashButton.grid(row=2, column=0)

        # Set up labels and fields for hash values
        Label(self.md5Frame, text="MD5: ").grid(row=0, column=0)
        Label(self.sha1Frame, text="SHA1: ").grid(row=0, column=0)
        Label(self.sha256Frame, text="SHA256: ").grid(row=0, column=0)
        self.md5Hash = Text(self.md5Frame, width=64, height=1)
        self.md5Hash.grid(row=0, column=1)
        self.md5Hash.insert(1.0, "NA")
        self.sha1Hash = Text(self.sha1Frame, width=64, height=1)
        self.sha1Hash.grid(row=0, column=1)
        self.sha1Hash.insert(1.0, "NA")
        self.sha256Hash = Text(self.sha256Frame, width=64, height=1)
        self.sha256Hash.grid(row=0, column=1)
        self.sha256Hash.insert(1.0, "NA")

    def SetupCVEParse(self):
        """Sets up and maintains the frame for retrieving list of CVEs from body text"""

        Label(self.cveBodySearchFrame, text="Input Text:").grid(row=1, column=0)
        self.bodyText = Text(self.cveBodySearchFrame, height=3, width=64)
        self.bodyText.grid(row=2, column=0)
        self.CVEparseButton = Button(
            self.cveBodySearchFrame, text="List CVEs", command=self.ParseCVEs)
        self.CVEparseButton.grid(row=3, column=0)
        Label(self.cveBodySearchFrame, text="CVEs Found:").grid(row=4, column=0)
        self.parsedText = Text(self.cveBodySearchFrame, height=3, width=64)
        self.parsedText.grid(row=5)

    def SetupCommandBuilder(self):
        """Sets up and maintains the frame for holding the notebook of different commands"""

        # set up notebook of commands
        self.commandNotebook = ttk.Notebook(self.commandBuilderFrame)
        self.commandNotebook.grid()

        # establish frames of notebook FOR
        self.commandFrames = []
        self.commandObjects = {} 
        self.commandFlags = {}
        self.scrollFrames = {}
        for key, value in self.json.items(): #FOR each command - each has own tab
            self.commandFrames.append(ttk.Frame(self.commandNotebook))
            self.commandNotebook.add(self.commandFrames[-1], text=self.json[key]["title"])

            #Populate flag frames
            self.commandFlags[f"{self.json[key]['title']}"] = []
            for i, flag in enumerate(self.json[key]["flags"]): 
                col = i // COL_MAX
                Label(self.commandFrames[-1], text=f'{flag[0]}*' if flag[1] == True else flag[0]).grid(row=(i-(COL_MAX*col)), column=(col*4), padx=5, pady=5)
                self.commandFlags[f"{self.json[key]['title']}"].append(Text(self.commandFrames[-1], height=1, width=32))
                self.commandFlags[f"{self.json[key]['title']}"][-1].grid(row=(i-(COL_MAX*col)), column=(col*4)+1)
            self.commandObjects[f"{self.json[key]['title']}"] = self.json[key]
            
            Button(self.commandFrames[-1], text="Build!", command=lambda: self.Build(self.commandObjects[self.commandNotebook.tab(self.commandNotebook.select(), "text")])).grid(column=(col*3), sticky='ew', ipadx=10, ipady=5)
        self.commandResults = Text(self.commandBuilderFrame, height=3, width=64)
        self.commandResults.grid(row=3)

    def Build(self, comm):
        """Constructs a command for use in CLI"""
        isSuccessful = True
        commandList = f'{comm["prepend"]}'
        for j, c in enumerate(self.commandFlags[comm["title"]]):
            if c.get(1.0, "end").strip() == "" and comm["flags"][j][1] == True: #if blank but required
                commandList = f'Required flag missing: {comm["flags"][j][2]}'
                isSuccessful = False
                break
            elif c.get(1.0, "end").strip() == "" and comm["flags"][j][1] == False: #if blank but not required
                pass
            else: #if not blank
                commandList += " "
                commandList += comm["flags"][j][2]
                commandList += f' "{c.get(1.0, "end").strip()}"'
        if isSuccessful:
            commandList += f' {comm["append"]}'
        self.commandResults.delete(1.0, "end")
        self.commandResults.insert(
            1.0, commandList)

        # # Build direct scan frame FOR
        # Label(self.directScanFrame, text="-u - Download URL").grid(row=3, column=0)
        # self.directH = Text(self.directScanFrame, height=2, width=64)
        # self.directH.grid(row=3, column=1)
        # self.directButton = Button(
        #     self.directScanFrame, text="Build!", command=self.DirectScan)
        # self.directButton.grid(row=4, columnspan=2, pady=10)
        # Label(self.directScanFrame, text="Result: ").grid(row=5, column=0)
        # self.directResult = Text(self.directScanFrame, height=2, width=64)
        # self.directResult.grid(row=5, column=1)

        # # build OSSBOM frame
        # Label(self.ossbomFrame,
        #       text="-f - repo location from bin \n(eg. repos/mypy)").grid(row=3, column=0)
        # self.ossbom_f = Text(self.ossbomFrame, height=1, width=64)
        # self.ossbom_f.grid(row=3, column=1)
        # Label(self.ossbomFrame,
        #       text="-A - Author \n(eg. Python Software Foundation)").grid(row=4, column=0)
        # self.ossbom_a = Text(self.ossbomFrame, height=1, width=64)
        # self.ossbom_a.grid(row=4, column=1)
        # Label(self.ossbomFrame,
        #       text="-N - Project Name \n(eg. mypy)").grid(row=5, column=0)
        # self.ossbom_n = Text(self.ossbomFrame, height=1, width=64)
        # self.ossbom_n.grid(row=5, column=1)
        # Label(self.ossbomFrame,
        #       text="-V - Version \n(eg. 1.0.1)").grid(row=6, column=0)
        # self.ossbom_v = Text(self.ossbomFrame, height=1, width=64)
        # self.ossbom_v.grid(row=6, column=1)
        # Label(self.ossbomFrame, text="-E - External References - Must include at least one. \nChoose from list here: https://cyclonedx.org/docs/1.4/json/#metadata_tools_items_externalReferences_items_type").grid(row=7, column=0, columnspan=2)
        # Label(self.ossbomFrame, text="Reference Item Type\n(eg. vcs)").grid(
        #     row=8, column=0)
        # self.ossbom_etype = Text(self.ossbomFrame, height=1, width=64)
        # self.ossbom_etype.grid(row=8, column=1)
        # Label(self.ossbomFrame, text="Reference Item Value\n(eg.https://www.github.com/author/project)").grid(row=9, column=0)
        # self.ossbom_evalue = Text(self.ossbomFrame, height=1, width=64)
        # self.ossbom_evalue.grid(row=9, column=1)

        # # result
        # self.ossbomBuildButton = Button(
        #     self.ossbomFrame, text="Build!", command=self.OSSBOM)
        # self.ossbomBuildButton.grid(row=10, columnspan=2, pady=10)
        # Label(self.ossbomFrame, text="Result: ").grid(row=11, column=0)
        # self.ossbomResult = Text(self.ossbomFrame, height=4, width=64)
        # self.ossbomResult.grid(row=11, column=1)

    def LowerText(self):
        """Lowers text of file hash, then displays that value in the self.result field"""
        self.done.config(text="Done!")
        self.result.delete(1.0, "end")
        self.result.insert(1.0, self.upperText.get().lower())
        # print(self.lower.cget("text"))

    def HashFile(self):
        """Retrieves MD5, SHA1, and SHA256 hashes for selected file"""
        try:
            # Get file name from user
            self.filename = filedialog.askopenfilename(initialdir="/",
                                                       title="Select a File",
                                                       filetypes=(("executables", "*.exe"), ("all files", "*.*")))
            self.hashFileName.config(text=self.filename)

            # md5
            self.md5Hash.delete(1.0, "end")
            result = subprocess.run(
                f'certutil -hashfile "{self.filename}" md5', stdout=subprocess.PIPE)
            self.md5Hash.insert(1.0, result.stdout.decode('utf-8'))
            self.md5Hash.delete(1.0, 2.0)
            self.md5Hash.delete(3.0, "end")

            # SHA1
            self.sha1Hash.delete(1.0, "end")
            result = subprocess.run(
                f'certutil -hashfile "{self.filename}" sha1', stdout=subprocess.PIPE)
            self.sha1Hash.insert(1.0, result.stdout.decode('utf-8'))
            self.sha1Hash.delete(1.0, 2.0)
            self.sha1Hash.delete(3.0, "end")

            # SHA256
            self.sha256Hash.delete(1.0, "end")
            result = subprocess.run(
                f'certutil -hashfile "{self.filename}" sha256', stdout=subprocess.PIPE)
            self.sha256Hash.insert(1.0, result.stdout.decode('utf-8'))
            self.sha256Hash.delete(1.0, 2.0)
            self.sha256Hash.delete(3.0, "end")

        except:
            print("Not happening, sport.")

    def ParseCVEs(self):
        """Parses body text to find CVEs, deletes duplicates, then creates comma-separated list of CVEs"""

        self.parsedText.delete(1.0, "end")
        cveRegex = re.compile(r'CVE-\d+-\d+', re.VERBOSE)
        self.parsedText.insert(1.0, ', '.join(
            list(set(cveRegex.findall(self.bodyText.get(1.0, "end"))))))

    

    def OSSBOM(self):
        """Constructs an OSSBOM command for use in CLI"""
        self.ossbomResult.delete(
            1.0, "end") 
        self.ossbomResult.insert(
            1.0, f'create_sbom.sh -f "{self.ossbom_f.get(1.0, "end").strip()}" -A "{self.ossbom_a.get(1.0, "end").strip()}" -N "{self.ossbom_n.get(1.0, "end").strip()}" -V "{self.ossbom_v.get(1.0, "end").strip()}" -E \'[{{"url":"{self.ossbom_evalue.get(1.0, "end").strip()}", "type":"{self.ossbom_etype.get(1.0, "end").strip()}"}}]\' -m -v')
