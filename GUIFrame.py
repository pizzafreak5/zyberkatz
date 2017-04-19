# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tegan Straley
# GUI Frame for Zyber Katz KATTZ project
# created for CSCI 4800, cyber security programming
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# file: GUIFrame.py
# Creates the front-end side of a port scanner with Python's tkinter libraries.



import tkinter as tk
import sys
from tkinter import filedialog
import GUIFunctions


# Font size for the title
LARGE_FONT = ("fixedsys", 18)
SMALL_FONT = ("arial", 7)
BUTTON_FONT = ("arial", 14)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class mainGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("KATTZraper")
        self.iconbitmap('sideprofileCat.ico') # Sets the upper left-hand logo

        container = tk.Frame(self)


        #~~~~~~MENU~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        menu = tk.Menu(self)
        self.config(menu=menu)  # what's under 'File' menu item
        KATZmenu = tk.Menu(menu)
        KATZmenu.add_command(label="About KATTZ", command=GUIFunctions.about)
        menu.add_cascade(label="Zyber Katz", menu=KATZmenu)


        fileMenu = tk.Menu(menu)
        menu.add_cascade(label="Menu", menu=fileMenu)
        fileMenu.add_command(label="Search", command=lambda: self.showFrame("StartPage"))
        fileMenu.add_command(label="Results",  command=lambda: self.showFrame("resultsPage"))
        fileMenu.add_command(label="Analytics",  command=lambda: self.showFrame("analyticsPage"))
        fileMenu.add_command(label="Import",  command=lambda: self.showFrame("importPage"))
        fileMenu.add_command(label="Export",  command=lambda: self.showFrame("exportPage"))
        fileMenu.add_command(label="Exit", command=self.quit)

        editMenu = tk.Menu(menu)  # what's under 'About' menu item
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="add something?")

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, resultsPage, analyticsPage, importPage, exportPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("StartPage")

    def showFrame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class StartPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.shared_data = {
            "entry1": tk.StringVar(),
            "entry2": tk.StringVar(),
            "entry3": tk.StringVar(),
            "entry4": tk.StringVar()
        }
        def newSearch():
            jobTitle = self.shared_data["entry1"].get()
            state = self.shared_data["entry2"].get()
            city = self.shared_data["entry3"].get()
            searchTitle = self.shared_data["entry4"].get()
            location = state + ", " + city

            if state.isalpha() & city.isalpha():
                GUIFunctions.newSearch(jobTitle, location, searchTitle)
            else:
                tk.messagebox.showerror("Error", "There is a number in your entry for State/City")


        self.frame0 = tk.Frame(self)
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)

        self.label = tk.Label(self.frame0, text="K.A.T.T.Z. web scraper", font=LARGE_FONT).grid(row=0, column=0, padx=20, pady=20)
        self.jobTitleEntry = tk.Label(self.frame1, text="Job Title").grid(row=1, padx=10, pady=2)
        self.entry1 = tk.Entry(self.frame1,textvariable=self.shared_data["entry1"]).grid(row=1, column=1, padx=10, pady=2)
        self.example1 = tk.Label(self.frame1, text = "ex: Software engineer", font = SMALL_FONT).grid(row=2, column= 1)
        self.stateEntry = tk.Label(self.frame1, text="State").grid(row=3,  padx=10, pady=2)
        self.entry2 = tk.Entry(self.frame1,textvariable=self.shared_data["entry2"]).grid(row=3, column=1, padx=10, pady=2)
        self.example2 = tk.Label(self.frame1, text = "ex: CO, Colorado, colorado", font = SMALL_FONT).grid(row=4, column= 1)
        self.CityEntry = tk.Label(self.frame1, text="City").grid(row=5,  padx=10, pady=2)
        self.entry3 = tk.Entry(self.frame1, textvariable=self.shared_data["entry3"]).grid(row=5, column=1, padx=10, pady=2)
        self.example3 = tk.Label(self.frame1, text = "ex: Denver, denver", font = SMALL_FONT).grid(row=6, column= 1)
        self.searchTitleEntry = tk.Label(self.frame1, text="Search Title").grid(row=7,  padx=10, pady=2)
        self.entry4 = tk.Entry(self.frame1, textvariable=self.shared_data["entry4"]).grid(row=7, column=1, padx=10, pady=2)
        self.example4 = tk.Label(self.frame1, text = "ex: SoftwareEngineerSept2017", font = SMALL_FONT).grid(row=8, column= 1)
        self.searchButton = tk.Button(self.frame2,  text="Search Indeed.com", font= BUTTON_FONT, command=newSearch).grid(row=9,padx=10, pady=10 )

        self.frame0.pack()
        self.frame1.pack()
        self.frame2.pack()



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class resultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def returnResults():
            search = self.savedSearch.get()
            GUIFunctions.returnResults(search)

        title = tk.Label(self, text="Results").pack(padx=10, pady=10)
        self.savedSearch = tk.StringVar(self)
        self.savedSearch.set("job Title")  # default saved search
        self.savedSearchOption = tk.OptionMenu(self, self.savedSearch, "Software Engineer", "Nurse")
        self.savedSearchOption.pack(padx=5, pady=5)
        self.resultsButton = tk.Button(self,  text="View results", command = returnResults,
                                       font=BUTTON_FONT).pack(padx=20, pady=20 )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class analyticsPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def newAnalyticSearch():
            search = self.savedSearch.get()
            graph = self.graphType.get()
            category = self.category.get()
            GUIFunctions.createPieChart(search,graph,category)

        title = tk.Label(self, text="Analytics\n\nSelect attributes for graphing").pack( padx=10, pady=10)
        self.savedSearch = tk.StringVar(self)
        self. savedSearch.set("Job title")  # default saved search
        self.savedSearchOption = tk.OptionMenu(self, self.savedSearch, "Software Engineer", "Nurse")
        self.savedSearchOption.pack( padx=5, pady=5)

        self.graphType = tk.StringVar(self)
        self.graphType.set("Graph")  # default graph type search
        self.graphTypeOption = tk.OptionMenu(self, self.graphType, "Pie", "Bar")
        self.graphTypeOption.pack( padx=5, pady=5)

        self.category = tk.StringVar(self)
        self.category.set("Category")  # default saved search
        self.categoryOptions = tk.OptionMenu(self, self.category, "Salary", "Job experience level", "Job type" )
        self.categoryOptions.pack( padx=5, pady=5)

        self.graphButton = tk.Button(self,  text="Create graph", font=BUTTON_FONT, command = newAnalyticSearch)
        self.graphButton.pack(padx=20, pady=20)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class importPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        savedSearch = tk.StringVar(self)
        savedSearch.set("Choose a Job Type")  # default saved search
        savedSearchOption = tk.OptionMenu(self, savedSearch, "Choose a Job Type", "software dev", "ER doctor")
        savedSearchOption.pack(padx=5, pady=5)
        entry3Button = tk.Button(self, text="Import search", command=GUIFunctions.output).pack(padx=5, pady=5)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class exportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        savedSearch = tk.StringVar(self)
        savedSearch.set("Choose a Job Type")  # default saved search
        savedSearchOption = tk.OptionMenu(self, savedSearch, "Choose a Job Type", "software dev", "ER doctor")
        savedSearchOption.pack(padx=5, pady=5)
        entry2Button = tk.Button(self, text="Export destination", command=GUIFunctions.output).pack(padx=5, pady=5)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
app = mainGUI()
app.mainloop()



