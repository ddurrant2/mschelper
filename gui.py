from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
import re
import sanitize
from datetime import date
from datetime import timedelta
import pyperclip
#from tkinter.tix import *

WIN_HEIGHT = 540
WIN_WIDTH = 960
COL_MAX = 8
MINI_COL_MAX = 2
CLIPBOARD_SCALE_FACTOR = 45

WINDOW_BAR = '#3F58C8'
WINDOW_BAR_TEXT = '#FFFFFF'
UPPER_NOTEBOOK_FILLER = '#95A1DB'
UPPER_TAB_INACTIVE = '#BAC6FF'
UPPER_TAB_ACTIVE = '#F0F3FF'
LOWER_NOTEBOOK_OUTLINE = '#6471A8'
ACTIVE_TAB_TEXT = '#000000'
FLAG_FILLER_TEXT = '#CACCD6'
BUILD_BUTTON_FILLER = '#BAC6FF'
BUILD_BUTTON_TEXT = '#000000'
STANDARD_BG = '#F0F3FF' 


class GUI:
    """
    The GUI class creates and maintains all Tkinter features of the app.
    """

    def __init__(self, json_file, init, mode):
        # self.TestJson(json_file)
        self.json = json_file
        """Initializes and creates the Tkinter window and Notebook sections"""
        global root
        root = Tk()
        try:
            self.clipboard_icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), "clipboard.png"))
            self.clipboard_icon = self.clipboard_icon.subsample(CLIPBOARD_SCALE_FACTOR, CLIPBOARD_SCALE_FACTOR)
        except:
            print("Failed to load image in current directory - attempting images directory.")
        try:
            self.clipboard_icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), "images\clipboard.png"))
            self.clipboard_icon = self.clipboard_icon.subsample(CLIPBOARD_SCALE_FACTOR, CLIPBOARD_SCALE_FACTOR)
        except:
            print("Failed to load images.")

        #Set document style
        s = ttk.Style()
        s.theme_create("yummy", parent="alt", settings={
            "Lower.TNotebook": {"configure": {"background": STANDARD_BG, "bordercolor": LOWER_NOTEBOOK_OUTLINE, "relief": "flat", "bordercolor": LOWER_NOTEBOOK_OUTLINE,
                                              "borderwidth": 0, "lightcolor": LOWER_NOTEBOOK_OUTLINE, "darkcolor": LOWER_NOTEBOOK_OUTLINE}},
            "Upper.TNotebook": {"configure": {"background": UPPER_NOTEBOOK_FILLER, "bordercolor": LOWER_NOTEBOOK_OUTLINE, "relief": "flat", "borderwidth": 0}},
            "Lower.TNotebook.Tab": {
                "configure": {"background": UPPER_TAB_INACTIVE, "angle": 0, "padding": [5,3], 
                              "font": ("Trebuchet MS", 10), "borderwidth": 1, "bordercolor": LOWER_NOTEBOOK_OUTLINE, "darkcolor": LOWER_NOTEBOOK_OUTLINE,
                              "lightcolor": LOWER_NOTEBOOK_OUTLINE, "relief": "flat"},
                "map": {"background": [("selected", UPPER_TAB_ACTIVE)]}
            },
            "Upper.TNotebook.Tab": {
                "configure": {"background": UPPER_TAB_INACTIVE, "angle": 0, "padding": [5,3], 
                              "font": ("Trebuchet MS", 10), "borderwidth": 0, "bordercolor": STANDARD_BG, "darkcolor": STANDARD_BG,
                              "lightcolor": STANDARD_BG, "relief": "flat"},
                "map": {"background": [("selected", UPPER_TAB_ACTIVE)]}
            },
            "TFrame": {"configure": {"background": STANDARD_BG}},
            "TLabel": {"configure": {"background": STANDARD_BG, "font": ("Trebuchet MS", 10)}},
            "Header.TLabel": {"configure": {"background": STANDARD_BG, "font": ("Trebuchet MS", 12), "anchor": "center"}},
            "Info.TFrame": {"configure": {"background": UPPER_NOTEBOOK_FILLER}},
            "Info.TLabel": {"configure": {"background": UPPER_NOTEBOOK_FILLER, "font": ("Trebuchet MS", 8)}},
            "TButton": {"configure": {"background": BUILD_BUTTON_FILLER, "font": ("Trebuchet MS", 10), "anchor": 'we', 
                                      "padding": [5,3], "relief": "raised", "bordercolor": "#000000"}},
            "TCombobox": {"configure": {"background": BUILD_BUTTON_FILLER, "font": ("Trebuchet MS", 10), "anchor": 'we', "bordercolor": "#ffffff"}},
            "CB.TFrame":{"configure": {"background": STANDARD_BG, "anchor": 'we'}},
            "TCheckbutton":{"configure": {"background": STANDARD_BG, "anchor": 'we', "font": ("Trebuchet MS", 10)}},
            "CTC.TButton":{"configure": {"background": STANDARD_BG, "relief": "flat", "pady": 5, "anchor": "news"}},
            "sub.TButton":{"configure": {"background": BUILD_BUTTON_FILLER, "anchor": "news", "padding": [3,1], "font":("Trebuchet MS", 8)}},
        })
        s.theme_use("yummy")

        #Format root window options
        root.geometry("+10+10")
        root.configure(background=UPPER_NOTEBOOK_FILLER,
                       width=WIN_WIDTH, height=WIN_HEIGHT)
        root.option_add('*tearOff', False)
        self.windowTitle = init["windowTitle"]
        root.title(self.windowTitle)
        root.resizable(False, False)
        self.buttonList = {}
        try:
            icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), f'{init["gifName"]}')) 
            root.iconphoto(True, icon)
        except:
            print("Failed to load image in current directory - attempting images directory.")
        try:
            icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), f'images\{init["gifName"]}')) 
            root.iconphoto(True, icon)
        except:
            print("Failed to load image.")

        #Set notebook
        self.notebook = ttk.Notebook(root, style="Upper.TNotebook")
        self.notebook.grid(sticky='ew', padx=5, pady=[10,0])
        self.SetupWindows(root, init)
        self.SetupCommandBuilder()
        self.SetupLower()
        self.SetupHash()
        self.SetupCVEParse()

        if mode == "mainloop":
            root.mainloop()
        else:
            root.update()

    def TestJson(self, json_file):
        """Test that a json has properly loaded."""
        for key, value in json_file.items():
            print(json_file[key]["title"])
            f'The {json_file[key]["title"]} command has the following flags:'
            for flag in json_file[key]["flags"]:
                print(f'{flag[0]}{"*" if flag[1] == True else ""}: {flag[2]}')

    def SetupWindows(self, root, init):
        """Initializes frames for each tab"""
        # Info footer
        self.infoFooter = ttk.Frame(root, style="Info.TFrame")

        # Create frames for each tab
        self.lowerFrame = ttk.Frame(self.notebook, width=WIN_WIDTH-25)
        self.hashFrame = ttk.Frame(self.notebook)
        self.commandBuilderFrame = ttk.Frame(self.notebook)
        self.cveBodySearchFrame = ttk.Frame(self.notebook)

        # add frames to notebook with tab names
        self.notebook.add(self.commandBuilderFrame, text="Command Builder")
        self.notebook.add(self.lowerFrame, text="Lowercase")
        self.notebook.add(self.hashFrame, text="Hash a File")
        self.notebook.add(self.cveBodySearchFrame, text="CVE Body Search")

        # Create content frames for each tab
        self.lowerContent = ttk.Frame(self.lowerFrame)
        self.lowerContent.grid(sticky='news')
        self.hashContent = ttk.Frame(self.hashFrame)
        self.hashContent.grid(sticky='news')
        self.commandBuilderContent = ttk.Frame(self.commandBuilderFrame)
        self.commandBuilderContent.grid(sticky='news')
        self.cveBodySearchContent = ttk.Frame(self.cveBodySearchFrame)
        self.cveBodySearchContent.grid(sticky='news')

        # Add descriptions to each tab
        ttk.Label(self.lowerContent, text="Find a Vendor Hash that's in caps? \nPaste it below to get the lower case version!", 
                  style="Header.TLabel").grid(pady=15, sticky='ew')
        ttk.Label(self.hashContent, text="Hash a file with ease! \nSelect your file below.", 
                  style="Header.TLabel").grid(pady=15, sticky='ew', columnspan=3)
        ttk.Label(self.commandBuilderContent, text="Handy tool for crafting CLI commands!", 
                  style="Header.TLabel").grid(padx=10, pady=15, sticky='ew')
        ttk.Label(self.cveBodySearchContent, text="Got a changelog with too many CVE's? \nPaste the whole body here to get a comma-separated list!", 
                  style="Header.TLabel").grid(pady=15, sticky='ew')
        self.infoFooter.grid(sticky='ns')
        ttk.Label(self.infoFooter, text=f"Created by {init['author']} - {init['version']} Beta", style="Info.TLabel").grid(sticky='ns')

    def SetupLower(self):
        """Sets up and maintains the frame for lowering a file hash"""

        # Entry field where users will put their uppercase hashes
        ttk.Label(self.lowerContent, text="Uppercase Hash:").grid(row=1, column=0)
        self.upperText = StringVar()
        self.upper = Entry(
            self.lowerContent, textvariable=self.upperText, width=64)
        self.upper.grid(row=3, column=0)

        # Button that carries out the .lower() method
        self.lowerButton = ttk.Button(
            self.lowerContent, text="Go", command=self.LowerText)
        self.lowerButton.grid(row=4, column=0, pady=10)
        self.buttonList[f"Lowercase{self.lowerButton.cget('text')}"] = self.lowerButton

        # Done message says that the operation is done.
        self.done = ttk.Label(self.lowerContent)
        self.done.grid(row=5, column=0)

        # Displays the result of the .lower() method
        ttk.Label(self.lowerContent, text="Lowercase Hash:").grid(row=6, column=0)
        self.result = Text(self.lowerContent, height=1, font=("Trebuchet MS", 10))
        self.result.grid(row=7, column=0, padx=10)

    def SetupHash(self):
        """Sets up and maintains the frame for retrieving file hashes"""
     
        # Set up label and button for finding file
        self.hashFileName = ttk.Label(self.hashContent, text="No file selected")
        self.hashFileName.grid(row=1, column=0, columnspan=3)
        self.hashButton = ttk.Button(
            self.hashContent, text="Select File", command=self.HashFile)
        self.hashButton.grid(row=2, column=0, columnspan=3)
        self.buttonList[f"Hash a File{self.hashButton.cget('text')}"] = self.hashButton

        # Set up labels and fields for hash values
        ttk.Label(self.hashContent, text="MD5: ").grid(row=3, column=0)
        ttk.Label(self.hashContent, text="SHA1: ").grid(row=4, column=0)
        ttk.Label(self.hashContent, text="SHA256: ").grid(row=5, column=0)
        self.md5Hash = Text(self.hashContent, width=64, height=1, font=("Trebuchet MS", 10))
        self.md5Hash.grid(row=3, column=1)
        self.md5Hash.insert(1.0, "NA")
        self.sha1Hash = Text(self.hashContent, width=64, height=1, font=("Trebuchet MS", 10))
        self.sha1Hash.grid(row=4, column=1)
        self.sha1Hash.insert(1.0, "NA")
        self.sha256Hash = Text(self.hashContent, width=64, height=1, font=("Trebuchet MS", 10))
        self.sha256Hash.grid(row=5, column=1)
        self.sha256Hash.insert(1.0, "NA")

        #Setup clipboard buttons for each row
        md5clipboard = ttk.Button(self.hashContent, image=self.clipboard_icon, command=lambda: self.CopyHashToClipboard("md5"), style="CTC.TButton")
        md5clipboard.grid(row=3, column=2)
        self.buttonList["md5"] = md5clipboard
        sha1clipboard = ttk.Button(self.hashContent, image=self.clipboard_icon, command=lambda: self.CopyHashToClipboard("sha1"), style="CTC.TButton")
        sha1clipboard.grid(row=4, column=2)
        self.buttonList["sha1"] = sha1clipboard
        sha256clipboard = ttk.Button(self.hashContent, image=self.clipboard_icon, command=lambda: self.CopyHashToClipboard("sha256"), style="CTC.TButton")
        sha256clipboard.grid(row=5, column=2)
        self.buttonList["sha256"] = sha256clipboard

        #Setup Copied to Clipboard messages for each row
        self.md5ctc = ttk.Label(self.hashContent, text="")
        self.md5ctc.grid(row=3, column=4)
        self.sha1ctc = ttk.Label(self.hashContent, text="")
        self.sha1ctc.grid(row=4, column=4)
        self.sha256ctc = ttk.Label(self.hashContent, text="")
        self.sha256ctc.grid(row=5, column=4)

    def SetupCVEParse(self):
        """Sets up and maintains the frame for retrieving list of CVEs from body text"""

        #Initialize CVE widgets
        ttk.Label(self.cveBodySearchContent, text="Input Text:").grid(row=1, column=0)
        self.bodyText = Text(self.cveBodySearchContent, height=3, width=64, font=("Trebuchet MS", 10))
        self.bodyText.grid(row=2, column=0)
        self.CVEparseButton = ttk.Button(
            self.cveBodySearchContent, text="List CVEs", command=lambda: self.ParseCVEs(self.bodyText, self.parsedText, True))
        self.CVEparseButton.grid(row=3, column=0)
        self.buttonList[f"CVE Body Search{self.CVEparseButton.cget('text')}"] = self.CVEparseButton
        self.CVEctc = ttk.Label(self.cveBodySearchContent, text="")
        self.CVEctc.grid(row=4, column=0)
        ttk.Label(self.cveBodySearchContent, text="CVEs Found:").grid(row=5, column=0)
        self.parsedText = Text(self.cveBodySearchContent, height=3, width=64, font=("Trebuchet MS", 10))
        self.parsedText.grid(row=6)

    def SetupCommandBuilder(self):
        """Sets up and maintains the frame for holding the notebook of different commands"""

        # set up notebook of commands
        self.commandNotebook = ttk.Notebook(self.commandBuilderContent, style="Lower.TNotebook")
        self.commandNotebook.grid(sticky='ew', ipadx=10, padx=50, pady=3)

        # establish frames of notebook
        self.commandFrames = []
        self.commandObjects = {} #one per command
        self.commandInputs = {}
        self.checkboxDicts = {} #the checkboxes in a single command flag
        for key, value in self.json.items(): # for each command in all json commands
            self.commandFrames.append(ttk.Frame(self.commandNotebook))
            self.commandNotebook.add(
                self.commandFrames[-1], text=self.json[key]["title"])

            # Populate flag frames
            self.commandInputs[self.json[key]['title']] = {} #one dict per command
            totalHeight = 0
            currentRow = 0
            ownFrames = {}
            for k, v in self.json[key]["flags"].items():
                currentColumn = (totalHeight // COL_MAX)*3
                chosenFrame = self.commandFrames[-1] #by default, draw to main frame
                    
                if "hidden" not in self.json[key]["flags"][k].keys():
                    ttk.Label(chosenFrame, text=f'{self.json[key]["flags"][k]["name"]}*' if self.json[key]["flags"][k]["required"] == True else self.json[key]["flags"][k]["name"]).grid(
                        row=currentRow, column=currentColumn, padx=[25,5], pady=5, rowspan=(self.json[key]["flags"][k]["height"] if "height" in self.json[key]["flags"][k].keys() else 1))
                if "widget" in self.json[key]["flags"][k].keys() and self.json[key]["flags"][k]["widget"] == "combobox":
                    self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}'] = ttk.Combobox(chosenFrame, width=30, font=("Trebuchet MS", 10))
                    self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}'].grid(
                        row=currentRow, column=currentColumn+1)
                    self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}']["values"] = self.json[key]["flags"][k]["values"]
                    self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}'].current(0)
                    if "tooltip" in self.json[key]["flags"][k].keys():
                        pass
                        # tip = Balloon(self.commandFrames[-1])
                        # tip.bind_widget(self.commandInputs[f'{self.json[key]["flags"][k]["name"]}'], balloonmsg=self.json[key]["flags"][k]["tooltip"])
                elif "widget" in self.json[key]["flags"][k].keys() and self.json[key]["flags"][k]["widget"] == "checkboxes":
                    #make frame
                    checkFrame = ttk.Frame(chosenFrame, style="CB.TFrame")
                    checkFrame.grid(row=currentRow, column=currentColumn+1, sticky='news')
                    #make list of checkbox variables
                    self.checkboxDicts[f'{self.json[key]["title"]}{self.json[key]["flags"][k]["name"]}buttons'] = []
                    self.checkboxDicts[f'{self.json[key]["title"]}{self.json[key]["flags"][k]["name"]}vars'] = []
                    #Create checkboxes
                    for checkframeIndex, check in enumerate(self.json[key]["flags"][k]["values"]):
                        self.checkboxDicts[f'{self.json[key]["title"]}{self.json[key]["flags"][k]["name"]}vars'].append(IntVar(value = 1 if "default" in self.json[key]["flags"][k].keys() and self.json[key]["flags"][k]["default"] == True else 0))
                        self.checkboxDicts[f'{self.json[key]["title"]}{self.json[key]["flags"][k]["name"]}buttons'].append(ttk.Checkbutton(checkFrame, text=check, takefocus=0, variable=self.checkboxDicts[f'{self.json[key]["title"]}{self.json[key]["flags"][k]["name"]}vars'][-1]))
                        #Grid checkboxes 2 or 3 wide
                        self.checkboxDicts[f'{self.json[key]["title"]}{self.json[key]["flags"][k]["name"]}buttons'][-1].grid(column=(checkframeIndex%MINI_COL_MAX), row=((checkframeIndex//MINI_COL_MAX)*2), sticky='w', padx=3)
                        # if "default" in self.json[key]["flags"][k].keys() and self.json[key]["flags"][k]["default"] == True:
                        #     self.checkboxDicts[f'{self.json[key]["flags"][k]["name"]}vars'][-1].select()
                elif self.json[key]["flags"][k]["name"] == "CVE": #hard code now, scale later
                    ownFrames[self.json[key]["flags"][k]["name"]] = ttk.Frame(chosenFrame)
                    ownFrames[self.json[key]["flags"][k]["name"]].grid(row=currentRow, column=currentColumn+1)
                    chosenFrame = ownFrames[self.json[key]["flags"][k]["name"]]
                    self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}'] = Text(chosenFrame, 
                                                                                       height=self.json[key]["flags"][k]["height"] if "height" in self.json[key]["flags"][k].keys() else 1, 
                                                                                       width=32, highlightbackground=FLAG_FILLER_TEXT, highlightcolor=ACTIVE_TAB_TEXT, highlightthickness=1, 
                                                                                       font=("Trebuchet MS", 10))
                    self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}'].grid()
                    CVEbutton = ttk.Button(chosenFrame, text="Parse CVE from Changelog", style="sub.TButton", command=lambda: self.ParseCVEs(self.commandInputs[self.commandNotebook.tab(self.commandNotebook.select(), "text")][f'{self.json[key]["flags"]["-cl CHANGELOG"]["name"]}'], self.commandInputs[self.commandNotebook.tab(self.commandNotebook.select(), "text")][f'{self.json[key]["flags"]["-cve CVE"]["name"]}'], False))
                    CVEbutton.grid()
                    self.buttonList[f"Command Builder{self.GetCurrentCommandTab()}Parse CVE from Changelog"] = CVEbutton
                    
                else:
                    self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}'] = Text(chosenFrame, 
                                                                                       height=self.json[key]["flags"][k]["height"] if "height" in self.json[key]["flags"][k].keys() else 1, 
                                                                                       width=32, highlightbackground=FLAG_FILLER_TEXT, highlightcolor=ACTIVE_TAB_TEXT, highlightthickness=1, 
                                                                                       font=("Trebuchet MS", 10))
                    if "hidden" not in self.json[key]["flags"][k].keys():
                        self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}'].grid(row=currentRow, column=currentColumn+1, rowspan=(self.json[key]["flags"][k]["height"] if "height" in self.json[key]["flags"][k].keys() else 1))
                    if "default" in self.json[key]["flags"][k].keys():
                        if self.json[key]["flags"][k]["name"] == "Publish Date":
                            self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}'].insert(1.0, self.Yesterday())
                        else:
                            self.commandInputs[self.json[key]['title']][f'{self.json[key]["flags"][k]["name"]}'].insert(1.0, self.json[key]["flags"][k]["default"])
                    if "tooltip" in self.json[key]["flags"][k].keys():
                        pass
                        # tip = Balloon(self.commandFrames[-1])
                        # tip.bind_widget(self.commandInputs[f'{self.json[key]["flags"][k]["name"]}'], balloonmsg=self.json[key]["flags"][k]["tooltip"])
                if "hidden" not in self.json[key]["flags"][k].keys():
                    totalHeight += (self.json[key]["flags"][k]["height"] if "height" in self.json[key]["flags"][k].keys() else 1)
                    currentRow = (currentRow + (self.json[key]["flags"][k]["height"] if "height" in self.json[key]["flags"][k].keys() else 1)) % COL_MAX
            self.commandObjects[self.json[key]['title']] = self.json[key]

            buildButton = ttk.Button(self.commandBuilderContent, text="Build", command=lambda: self.Build(self.commandObjects[self.commandNotebook.tab(
                self.commandNotebook.select(), "text")]))
            buildButton.grid(row=3, pady=5)
            self.buttonList[f"Command Builder{self.json[key]['title']}{buildButton.cget('text')}"] = buildButton
        self.commandBuilderCTC = ttk.Label(self.commandBuilderContent, text="")
        self.commandBuilderCTC.grid(row=4)
        self.commandResults = Text(
            self.commandBuilderContent, height=6, width=64, font=("Trebuchet MS", 10))
        self.commandResults.grid(row=5, padx=10, pady=[5,10], sticky='news')

    def Build(self, comm): #comm = entire command dictionary for panel on which build button was pushed
        """Constructs a command for use in CLI"""
        isSuccessful = True
        commandOutput = f'{comm["prepend"]}'
        for keys, values in comm["flags"].items(): #for each flag in the specified command
            #if combo or radio
            if "widget" in comm["flags"][keys].keys() and (comm["flags"][keys]["widget"] == "combobox" or comm["flags"][keys]["widget"] == "radio"):
                commandOutput += f' {comm["flags"][keys]["flag"]} "{self.commandInputs[comm["title"]][comm["flags"][keys]["name"]].get()}"'
            #if checkbutton
            elif "widget" in comm["flags"][keys].keys() and comm["flags"][keys]["widget"] == "checkboxes":
                readValues = []
                for x in self.checkboxDicts[f'{comm["title"]}{comm["flags"][keys]["name"]}vars']:
                    readValues.append(x.get())
                    #print(readValues)
                if "sanitizeFunction" in comm["flags"][keys].keys():
                    func = getattr(sanitize, comm["flags"][keys]["sanitizeFunction"])
                    commandOutput += f' {func(readValues, comm["flags"][keys]["flags"])}'
                else:
                    for index, var in enumerate(readValues):
                        if var == 1:
                            self.checkboxDicts[f'{comm["title"]}{comm["flags"][keys]["name"]}vars']
                            commandOutput += f' {comm["flags"][keys]["flags"][index]}'
            # if blank but required
            elif self.commandInputs[f"{comm['title']}"][comm["flags"][keys]["name"]].get(1.0, "end").strip() == "" and comm["flags"][keys]["required"] == True:
                commandOutput = f'Required field missing: {comm["flags"][keys]["name"]}'
                isSuccessful = False
                break
            # if blank but not required
            elif self.commandInputs[f"{comm['title']}"][comm["flags"][keys]["name"]].get(1.0, "end").strip() == "" and comm["flags"][keys]["required"] == False:
                if "sanitizeFunction" in comm["flags"][keys].keys():
                    func = getattr(sanitize, comm["flags"][keys]["sanitizeFunction"])
                    funcResult = func([self.commandInputs[comm['title']][comm["flags"][x]["name"]].get(1.0, "end") for x in comm["flags"][keys]["sanitizeParameters"]])
                    if funcResult != "":
                        commandOutput += f' {comm["flags"][keys]["flag"]} "{funcResult}"'
                
            # if not blank
            else:  
                commandOutput += " "
                commandOutput += comm["flags"][keys]["flag"]
                flagOutput = self.commandInputs[comm['title']][comm["flags"][keys]["name"]].get(1.0, "end").strip().replace("\n", "\\n")
                if "sanitizeFunction" in comm["flags"][keys].keys():
                    func = getattr(sanitize, comm["flags"][keys]["sanitizeFunction"])
                    commandOutput += f' "{func([self.commandInputs[comm["title"]][comm["flags"][x]["name"]].get(1.0, "end") for x in comm["flags"][keys]["sanitizeParameters"]])}"'
                else:
                    commandOutput += f' "{flagOutput}"'
        if isSuccessful:
            commandOutput += f' {comm["append"]}'
            pyperclip.copy(commandOutput)
            self.commandBuilderCTC.config(text="Copied to Clipboard!")
        self.commandResults.delete(1.0, "end")
        self.commandResults.insert(
            1.0, commandOutput)
        

    def LowerText(self):
        """Lowers text of file hash, then displays that value in the self.result field"""
        self.done.config(text="Copied to Clipboard")
        self.result.delete(1.0, "end")
        self.result.insert(1.0, self.upperText.get().lower())
        pyperclip.copy(self.upperText.get().lower())

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
            self.md5Hash.delete(3.0, "end")
            self.md5Hash.delete(1.0, 2.0)

            # SHA1
            self.sha1Hash.delete(1.0, "end")
            result = subprocess.run(
                f'certutil -hashfile "{self.filename}" sha1', stdout=subprocess.PIPE)
            self.sha1Hash.insert(1.0, result.stdout.decode('utf-8'))
            self.sha1Hash.delete(3.0, "end")
            self.sha1Hash.delete(1.0, 2.0)

            # SHA256
            self.sha256Hash.delete(1.0, "end")
            result = subprocess.run(
                f'certutil -hashfile "{self.filename}" sha256', stdout=subprocess.PIPE)
            self.sha256Hash.insert(1.0, result.stdout.decode('utf-8'))
            self.sha256Hash.delete(3.0, "end")
            self.sha256Hash.delete(1.0, 2.0)

        except:
            print("Error hashing.") #replace with error pop-up?

    def CopyHashToClipboard(self, valueToCopy): 
        if valueToCopy == "md5":
            self.ClearClipboardMessages()
            self.md5ctc.config(text="Copied to Clipboard")
            pyperclip.copy(self.md5Hash.get(1.0, "end").strip())
        elif valueToCopy == "sha1":
            self.ClearClipboardMessages()
            self.sha1ctc.config(text="Copied to Clipboard")
            pyperclip.copy(self.sha1Hash.get(1.0, "end").strip())
        elif valueToCopy == "sha256":
            self.ClearClipboardMessages()
            self.sha256ctc.config(text="Copied to Clipboard")
            pyperclip.copy(self.sha256Hash.get(1.0, "end").strip())
        else:
            print("Error copying hash to clipboard")

    def ClearClipboardMessages(self):
        self.md5ctc.config(text="")
        self.sha1ctc.config(text="")
        self.sha256ctc.config(text="")

    def ParseCVEs(self, inputTextWidget, outputTextWidget, isCVEPane):
        """Parses body text to find CVEs, deletes duplicates, then creates comma-separated list of CVEs"""
        outputTextWidget.delete(1.0, "end")
        cveRegex = re.compile(r'CVE-\d+-\d+', re.VERBOSE)
        outputTextWidget.insert(1.0, ', '.join(
            list(set(cveRegex.findall(inputTextWidget.get(1.0, "end"))))))
        if isCVEPane:
            pyperclip.copy(outputTextWidget.get(1.0, "end").strip())
            self.CVEctc.config(text="Copied to Clipboard!")
        
    def Yesterday(self):
        """Returns the date of the previous workday."""
        if date.today().weekday() == 0:
            return (date.today() - timedelta(days = 3))
        else:
            return (date.today() - timedelta(days = 1))
        
    def UpdateRoot(self):
        """Used to manually update the GUI in lieu of root.mainloop()"""
        root.update()

    def GetAllTabs(self):
        """Returns all tab names in the notebook."""
        return [self.notebook.tab(i, option='text') for i in self.notebook.tabs()]

    def GetCurrentNBTab(self):
        """Returns the name of the currently-selected notebook tab."""
        return self.notebook.tab(self.notebook.select(), "text")
    
    def GetCurrentCommandTab(self):
        """Returns the name of the currently-selected Command Builder tab."""
        if self.notebook.tab(self.notebook.select(), option='text') == "Command Builder":
            return self.commandNotebook.tab(self.commandNotebook.select(), option='text')
        else:
            return "Not currently in Command Tab."

    def GetAllCommandTabs(self):
        """Returns all tab names in the Command Builder pane."""
        if self.notebook.tab(self.notebook.select(), option='text') == "Command Builder":
            return [self.commandNotebook.tab(i, option='text') for i in self.commandNotebook.tabs()]
        else:
            return "Not currently in Command Tab."
    
    def CloseWindow(self):
        """Closes the entire current Tkinter GUI."""
        try: 
            root.destroy()
            return "Closed Window."
        except:
            return "Error closing Window."
    
    def SwapTab(self, tablevel, tabname):
        """Swap from one notebook tab to another. 
        Requires tablevel (0 for main notebook, 1 for Command Builder), and 
        tabname, the name of the desired tab as it appears in the GUI."""
        if tablevel == 0:
            selectedNotebook = self.notebook
        elif tablevel == 1:
            selectedNotebook = self.commandNotebook
        else:
            return "Invalid notebook selection index."
        if tabname in [selectedNotebook.tab(i, option='text') for i in selectedNotebook.tabs()]:
            selectedNotebook.select([selectedNotebook.tab(i, option='text') for i in selectedNotebook.tabs()].index(tabname))
            self.UpdateRoot()
            return f"New tab opened: {selectedNotebook.tab(selectedNotebook.select(), option='text')}"
        else:
            return "Tab name not recognized."

    def SetText(self, field, input):
        """This method sets any text field in the current tab. 
        Requires field, which is the label that appears next to the desired field, and
        input, which is the desired text to be written in that field."""
        try:
            self.commandInputs[self.commandNotebook.tab(self.commandNotebook.select(), option='text')][field].delete(1.0, "end")
            self.commandInputs[self.commandNotebook.tab(self.commandNotebook.select(), option='text')][field].insert(1.0, input)
            return "Successfully wrote to text"
        except:
            return "Error - did not find specified key on this tab."

    def GetText(self, field):
        """This method returns the value of any given field in the current tab.
        Requires field, which is the label that appears next to the desired field."""
        try:
            return self.commandInputs[self.commandNotebook.tab(self.commandNotebook.select(), option='text')][field].get(1.0, "end").strip()
        except:
            return "Error - did not find specified key on this tab."
        
    def FillFields(self, fieldDict):
        """This method sets multiple text fields at the same time. 
        Requires fieldDict, a dictionary of field names: desired values."""
        for k, v in fieldDict.items():
            if self.SetText(k, v) == "Error - did not find specified key on this tab.":
                return f"Encountered error writing {v} to {k}."
        return "Successfully wrote to all fields."

    def SetCheckbox(self, parent, field, input):
        """ This method sets the value of a checkbox. 
        Requires 'parent', which is the name next to all related checkboxes (ie File Classification),
        'field', or label next to the specific checkbox (ie Bugfix), and 
        input, with 0 for off, 1 for on."""
        try:
            for index, x in enumerate(self.checkboxDicts[f'{self.GetCurrentCommandTab()}{parent}buttons']):
                if x.cget("text") == field: 
                    self.checkboxDicts[f'{self.GetCurrentCommandTab()}{parent}vars'][index].set(input)
                    self.UpdateRoot()
                    return f"Successfully set checkbox to {'True' if input == 1 else 'False'}"
            return "No flag exists with that parent."
        except:
            return "Error - did not find specified key on this tab."

    def GetCheckbox(self, parent, field):
        """Returns the value of any selected checkbox.
        Requires parent, or the label to the left of all related checkboxes, and
        field, or the label to the right of the specific checkbox."""
        try:
            for index, x in enumerate(self.checkboxDicts[f'{self.GetCurrentCommandTab()}{parent}buttons']):
                if x.cget("text") == field:
                    return "True" if self.checkboxDicts[f'{self.GetCurrentCommandTab()}{parent}vars'][index].get() == 1 else "False"
            return "Field not found in Parent."
        except:
            return "Error - did not find specified checkbox on this tab."

    def SetCombobox(self, field, input):
        """This method sets a combobox to a value within its assigned values.
        Requires field, which is the label that appears next to the desired combobox, and
        input, which is the desired value from the dropdown."""
        try:
            if input in self.commandInputs[self.GetCurrentCommandTab()][field]["values"]:
                self.commandInputs[self.GetCurrentCommandTab()][field].set(input)
                return f"Successfully wrote {input} to {field}."
            else:
                return "Error - invalid value for this combobox."
        except:
            return "Error writing to combobox."

    def GetCombobox(self, field):
        """This method the value of a combobox.
        Requires field, which is the label that appears next to the desired combobox."""
        try:
            return self.commandInputs[self.GetCurrentCommandTab()][field].get()
        except:
            return "Error retrieving combobox value."

    def PushButton(self, upperTab, lowerTab, buttonText):
        """This method pushes a button on the given tab.
        Requires upperTab, or the title of the tab in the main Notebook,
        lowerTab, or the title of the tab in the Command Builder pane, and
        buttonText, or the text that appears in the desired button."""
        self.SwapTab(0, upperTab)
        if lowerTab != "":
            self.SwapTab(1, lowerTab)
        try:
            self.buttonList[f"{upperTab}{lowerTab}{buttonText}"].invoke()
            return f"Pushed {buttonText} on {self.GetCurrentNBTab()}{self.GetCurrentCommandTab() if self.GetCurrentNBTab() == 'Command Builder' else ''}"
        except:
            return f"Error finding the {buttonText} button on {self.GetCurrentNBTab()}{self.GetCurrentCommandTab() if self.GetCurrentNBTab() == 'Command Builder' else ''}"

    def GetResult(self):
        """This method returns the main output of the currently-selected pane.
        For other text fields, please use GetText()."""
        if self.GetCurrentNBTab() == "Command Builder":
            return self.commandResults.get(1.0, "end").strip()
        elif self.GetCurrentNBTab() == "Lowercase":
            return self.result.get(1.0, "end").strip()
        elif self.GetCurrentNBTab() == "CVE Body Search":
            return self.parsedText.get(1.0, "end").strip()
        else:
            return "Error retrieving or GetResult not supported on this tab."

