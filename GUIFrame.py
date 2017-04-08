# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tegan Straley
# GUI Frame for Zyber Katz KATTZ project
# created for CSCI 4800, cyber security programming
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# file: GUIFrame.py
# Creates the front-end side of a port scanner with Python's tkinter libraries.
# Pack and grid inserts are found at the bottom of the file.



import tkinter as tk
import sys
from tkinter import filedialog
#from GUIFunctions import *
import GUIFunctions


LARGE_FONT = ("fixedsys", 18)

class mainGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("KATTZraper");
        self.iconbitmap('sideprofileCat.ico')

        container = tk.Frame(self)


        #~~~~~~MENU~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        menu = tk.Menu(self)
        self.config(menu=menu)  # what's under 'File' menu item
        KATZmenu = tk.Menu(menu)
        KATZmenu.add_command(label="About KATTZ", command=GUIFunctions.about)
        menu.add_cascade(label="Zyber Katz", menu=KATZmenu)


        fileMenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Search", command=lambda: self.showFrame(StartPage))
        fileMenu.add_command(label="Results",  command=lambda: self.showFrame(resultsPage))
        fileMenu.add_command(label="Analytics",  command=lambda: self.showFrame(analyticsPage))
        fileMenu.add_command(label="Import",  command=lambda: self.showFrame(importPage))
        fileMenu.add_command(label="Export",  command=lambda: self.showFrame(exportPage))
        fileMenu.add_command(label="Exit", command=self.quit)

        editMenu = tk.Menu(menu)  # what's under 'About' menu item
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="add something?")

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, resultsPage, analyticsPage, importPage, exportPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frame0 = tk.Frame(self)
        frame1 = tk.Frame(self)
        frame2 = tk.Frame(self)
        label = tk.Label(frame0, text="K.A.T.T.Z. web scraper", font=LARGE_FONT).grid(row=0, column=0, padx=20, pady=20)
        jobTitleEntry = tk.Label(frame1, text="Job type").grid(row=1, padx=10, pady=10)
        entry1 = tk.Entry(frame1, text="").grid(row=1, column=1, padx=10, pady=10)
        stateEntry = tk.Label(frame1, text="State").grid(row=2,  padx=10, pady=10)
        entry2 = tk.Entry(frame1).grid(row=2, column=1, padx=10, pady=10)
        CityEntry = tk.Label(frame1, text="City").grid(row=3,  padx=10, pady=10)
        entry3 = tk.Entry(frame1).grid(row=3, column=1, padx=10, pady=10)
        searchButton = tk.Button(frame2, text="Search Indeed.com").grid(row=4,padx=10, pady=10 )  # center the search button?

        frame0.pack()
        frame1.pack()
        frame2.pack()


class resultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Choose a job type").grid(row=0, column=0, padx=10, pady=10)
        savedSearch = tk.StringVar(self)
        savedSearch.set("search")  # default saved search
        savedSearchOption = tk.OptionMenu(self, savedSearch, "software", "engineer")
        savedSearchOption.grid(row=1, column=0, padx=5, pady=5)


class analyticsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Choose a job type").grid(row=0, column=0, padx=10, pady=10)
        savedSearch = tk.StringVar(self)
        savedSearch.set("search")  # default saved search
        savedSearchOption = tk.OptionMenu(self, savedSearch, "search", "two")
        savedSearchOption.grid(row=1, column=0, padx=5, pady=5)


class importPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        savedSearch = tk.StringVar(self)
        savedSearch.set("Choose a Job Type")  # default saved search
        savedSearchOption = tk.OptionMenu(self, savedSearch, "Choose a Job Type", "software dev", "ER doctor")
        savedSearchOption.pack(padx=5, pady=5)
        entry3Button = tk.Button(self, text="Import search", command=GUIFunctions.output).pack(padx=5, pady=5)


class exportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        savedSearch = tk.StringVar(self)
        savedSearch.set("Choose a Job Type")  # default saved search
        savedSearchOption = tk.OptionMenu(self, savedSearch, "Choose a Job Type", "software dev", "ER doctor")
        savedSearchOption.pack(padx=5, pady=5)
        entry2Button = tk.Button(self, text="Export destination", command=GUIFunctions.output).pack(padx=5, pady=5)


app = mainGUI()
app.mainloop()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def newSearch(self):
#     StartPage
