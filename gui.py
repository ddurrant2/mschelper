from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
import re
import webbrowser
import pathlib

version = "v0.3 pre-alpha"
# bgColor = '#f0f5ff'


class GUI:
    """
    The GUI class creates and maintains all Tkinter features of the app.
    """

    def __init__(self):
        """Initializes and creates the Tkinter window and Notebook sections"""
        root = Tk()
        root.option_add('*tearOff', False)
        root.title("SOFIA - Support Over FIA")
        root.resizable(False, False)
        icon = PhotoImage(
            file=f"{pathlib.Path().parent.absolute()}\\squarelogo.gif") #file="C:\\Users\\ddurrant\\Documents\\squarelogo.gif"
        root.iconphoto(True, icon)
        self.notebook = ttk.Notebook(root, height=450, width=800)
        self.notebook.grid()
        self.SetupWindows(root)
        self.SetupLower()
        self.SetupHash()
        self.SetupCVEParse()
        self.SetupCommandBuilder()

        root.mainloop()

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
        self.notebook.add(self.lowerFrame, text="Lower()")
        self.notebook.add(self.hashFrame, text="Hash a File")
        self.notebook.add(self.cveBodySearchFrame, text="CVE Body Search")
        self.notebook.add(self.commandBuilderFrame, text="Command Builder")

        # Add descriptions to each tab
        Label(self.lowerFrame, text="Find a Vendor Hash that's in caps? \nPaste it below to get the lower case version!", font=(
            "Helvetica", 12)).grid(pady=15)
        Label(self.hashFrame, text="Hash a file with ease! \nSelect your file below.", font=(
            "Helvetica", 12)).grid(pady=15)
        Label(self.commandBuilderFrame, text="Handy tool for crafting CLI commands!", font=(
            "Helvetica", 12)).grid(pady=15)
        Label(self.cveBodySearchFrame, text="Got a changelog with too many CVE's? \nPaste the whole body here and we'll give you a comma-separated list!",
              font=("Helvetica", 12)).grid(pady=15)
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

        # establish frames of notebook
        self.directScanFrame = ttk.Frame(self.commandNotebook)
        self.commandNotebook.add(self.directScanFrame, text="Direct Scan")
        self.ossbomFrame = ttk.Frame(self.commandNotebook)
        self.commandNotebook.add(self.ossbomFrame, text="OSSBOM")

        # Hyperlink functions
        def callback(url):
            webbrowser.open_new_tab(url)

        # Build direct scan frame
        directDocs = Label(
            self.directScanFrame, text="Direct Scan - Click to view Documentation", fg="blue", cursor="hand2")
        directDocs.grid(row=0, columnspan=2)
        directDocs.bind("<Button-1>", lambda e: callback(
            "https://fortressinfosec.atlassian.net/wiki/spaces/FIAOpsKB/pages/4026630450/CLI+Registrations"))
        Label(self.directScanFrame, text="-u - Download URL").grid(row=3, column=0)
        self.directH = Text(self.directScanFrame, height=2, width=64)
        self.directH.grid(row=3, column=1)
        self.directButton = Button(
            self.directScanFrame, text="Build!", command=self.DirectScan)
        self.directButton.grid(row=4, columnspan=2, pady=10)
        Label(self.directScanFrame, text="Result: ").grid(row=5, column=0)
        self.directResult = Text(self.directScanFrame, height=2, width=64)
        self.directResult.grid(row=5, column=1)

        # build OSSBOM frame
        ossbomDocs = Label(
            self.ossbomFrame, text="OSSBOM - Click to view Documentation", fg="blue", cursor="hand2")
        ossbomDocs.grid(row=0, columnspan=2)
        ossbomDocs.bind("<Button-1>", lambda e: callback(
            "https://fortressinfosec.atlassian.net/wiki/spaces/FIAOpsKB/pages/4021649657/OSSBOM+Walkthrough"))

        # Set up flags
        Label(self.ossbomFrame,
              text="-f - repo location from bin \n(eg. repos/mypy)").grid(row=3, column=0)
        self.ossbom_f = Text(self.ossbomFrame, height=1, width=64)
        self.ossbom_f.grid(row=3, column=1)
        Label(self.ossbomFrame,
              text="-A - Author \n(eg. Python Software Foundation)").grid(row=4, column=0)
        self.ossbom_a = Text(self.ossbomFrame, height=1, width=64)
        self.ossbom_a.grid(row=4, column=1)
        Label(self.ossbomFrame,
              text="-N - Project Name \n(eg. mypy)").grid(row=5, column=0)
        self.ossbom_n = Text(self.ossbomFrame, height=1, width=64)
        self.ossbom_n.grid(row=5, column=1)
        Label(self.ossbomFrame,
              text="-V - Version \n(eg. 1.0.1)").grid(row=6, column=0)
        self.ossbom_v = Text(self.ossbomFrame, height=1, width=64)
        self.ossbom_v.grid(row=6, column=1)
        Label(self.ossbomFrame, text="-E - External References - Must include at least one. \nChoose from list here: https://cyclonedx.org/docs/1.4/json/#metadata_tools_items_externalReferences_items_type").grid(row=7, column=0, columnspan=2)
        Label(self.ossbomFrame, text="Reference Item Type\n(eg. vcs)").grid(
            row=8, column=0)
        self.ossbom_etype = Text(self.ossbomFrame, height=1, width=64)
        self.ossbom_etype.grid(row=8, column=1)
        Label(self.ossbomFrame, text="Reference Item Value\n(eg.https://www.github.com/author/project)").grid(row=9, column=0)
        self.ossbom_evalue = Text(self.ossbomFrame, height=1, width=64)
        self.ossbom_evalue.grid(row=9, column=1)

        # result
        self.ossbomBuildButton = Button(
            self.ossbomFrame, text="Build!", command=self.OSSBOM)
        self.ossbomBuildButton.grid(row=10, columnspan=2, pady=10)
        Label(self.ossbomFrame, text="Result: ").grid(row=11, column=0)
        self.ossbomResult = Text(self.ossbomFrame, height=4, width=64)
        self.ossbomResult.grid(row=11, column=1)

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

    def DirectScan(self):
        """Constructs a Direct Registration command for use in CLI"""
        self.directResult.delete(1.0, "end")
        self.directResult.insert(
            1.0, f"python3 fiayeeter.py -i -u {self.directH.get(1.0, 'end')}")

    def OSSBOM(self):
        """Constructs an OSSBOM command for use in CLI"""
        self.ossbomResult.delete(
            1.0, "end") 
        self.ossbomResult.insert(
            1.0, f'create_sbom.sh -f "{self.ossbom_f.get(1.0, "end").strip()}" -A "{self.ossbom_a.get(1.0, "end").strip()}" -N "{self.ossbom_n.get(1.0, "end").strip()}" -V "{self.ossbom_v.get(1.0, "end").strip()}" -E \'[{{"url":"{self.ossbom_evalue.get(1.0, "end").strip()}", "type":"{self.ossbom_etype.get(1.0, "end").strip()}"}}]\' -m -v')
