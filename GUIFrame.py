#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Tegan Straley
#GUI Frame for Zyber Katz KATTZ project
#created for CSCI 4800, cyber security programming
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# file: GUIFrame.py
# Creates the front-end side of a port scanner with Python's tkinter libraries.
# Pack and grid inserts are found at the bottom of the file.

# Resources : http://code.activestate.com/recipes/577261-python-tkinter-tabs/

from tkinter import *
from tkinter import filedialog
import GUIFunctions

#~~~~~~~~~~ TAB FUNCTIONALITY ~~~~~~~~~~

BASE = RAISED
SELECTED = FLAT


# a base tab class
class Tab(Frame):
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.tab_name = name


# the bulk of the logic is in the actual tab bar
class TabBar(Frame):
    def __init__(self, master=None, init_name=None):
        Frame.__init__(self, master)
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name

    def show(self):
        self.pack(side=TOP, expand=YES, fill=X)
        self.switch_tab(self.init_name or self.tabs.keys()[-1])  # switch the tab to the first tab

    def add(self, tab):
        tab.pack_forget()  # hide the tab on init

        self.tabs[tab.tab_name] = tab  # add it to the list of tabs
        b = Button(self, text=tab.tab_name, relief=BASE,  # basic button stuff
                   command=(lambda name=tab.tab_name: self.switch_tab(name)))  # set the command to switch tabs
        b.pack(side=LEFT)  # pack the buttont to the left mose of self
        self.buttons[tab.tab_name] = b  # add it to the list of buttons

    def delete(self, tabname):

        if tabname == self.current_tab:
            self.current_tab = None
            self.tabs[tabname].pack_forget()
            del self.tabs[tabname]
            self.switch_tab(self.tabs.keys()[0])

        else:
            del self.tabs[tabname]

        self.buttons[tabname].pack_forget()
        del self.buttons[tabname]

    def switch_tab(self, name):
        if self.current_tab:
            self.buttons[self.current_tab].config(relief=BASE)
            self.tabs[self.current_tab].pack_forget()  # hide the current tab
        self.tabs[name].pack(side=BOTTOM)  # add the new tab to the display
        self.current_tab = name  # set the current tab to itself

        self.buttons[name].config(relief=SELECTED)


#~~~~~~~~~~ MENU ~~~~~~~~~~

# root = Tk()
#
# menu = Menu(root)
# root.config(menu=menu) # what's under 'File' menu item
# fileMenu = Menu(menu)
# menu.add_cascade(label="File", menu=fileMenu)
# fileMenu.add_command(label="lorem pdsem")
# fileMenu.add_separator()
# fileMenu.add_command(label="Exit", command=root.quit)
#
# aboutMenu = Menu(menu) # what's under 'About' menu item
# menu.add_cascade(label="About", menu=aboutMenu)
# aboutMenu.add_command(label="Author")
# aboutMenu.add_command(label="Zyber Katz")
#
# #~~~~~~~~ TABS CREATION ~~~~~~~~
#
# bar = TabBar(root, "Search")
# tab1 = Tab(root, "tab1")
# label = Label(tab1, text="K.A.T.T.Z. web scraper")
# # things for scannerInfo2
# jobTitleEntry = Label(tab1, text="Job title")
# entry1 = Entry(tab1)
# stateEntry = Label(tab1, text="State")
# entry2 = Entry(tab1)
# CityEntry = Label(tab1, text="City")
# entry3 = Entry(tab1)
# NameOfSearchEntry = Label(tab1, text="Name this search")
# entry4 = Entry(tab1)
#
#
# #~~~~~~~~ FEATURE CREATION ~~~~~~~~
#
# # scannerInfo = Frame(root)
# # scannerInfo2 = Frame(root)
# # scannerInfo3 = Frame(root)
#
#
# # things for scannerInfo3
# scan_button = Button(tab1, text="Search Indeed.com", width = 20, height = 1)
#
# #~~~~~~~~~~ LAYOUT PACK, GRID, ETC. ~~~~~~~~~~~~~
#
# #scannerInfo
# label.pack(fill=X, pady=10)
#
# #scannerInfo2
# # jobTitleEntry.grid(row=1, sticky=E, padx = 5, pady=5)
# # entry1.grid(row=1, column=1, sticky=E, padx = 5, pady=5)
# # stateEntry.grid(row=2, sticky=E, padx = 5, pady=5)
# # entry2.grid(row=2, column=1, sticky=E, padx = 5, pady=5)
# # CityEntry.grid(row=3, sticky=E, padx = 5, pady=5)
# # entry3.grid(row=3, column=1, sticky=E, padx = 5, pady=5)
# # NameOfSearchEntry.grid(row=3, sticky=E, padx = 5, pady=5)
# # entry4.grid(row=3, column=1, sticky=E, padx = 5, pady=5)
#
# #scannerInfo3
# scan_button.pack(padx = 10, pady=10)
#
# # scannerInfo.pack()
# # scannerInfo2.pack()
# # scannerInfo3.pack()
#
# bar.add(tab1)
#
#
# root.title("Zyber Katz K.A.T.T.Z. web scrapper")
#
# bar.show()
# mainloop() # shows the GUI

if __name__ == '__main__':

    root = Tk()

    root.title("KATTZraper");
    #root.geometry('500x500')

    menu = Menu(root)
    root.config(menu=menu)  # what's under 'File' menu item
    fileMenu = Menu(menu)
    menu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New Search", command=GUIFunctions.NewSearch())
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=root.quit)

    aboutMenu = Menu(menu)  # what's under 'About' menu item
    menu.add_cascade(label="About", menu=aboutMenu)
    aboutMenu.add_command(label="Author")
    aboutMenu.add_command(label="Zyber Katz")

    bar = TabBar(root, "Search")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    tab1 = Tab(root, "Search")  # notice how this one's master is the root instead of the bar
    #frame1 = Frame(tab1)
    label = Label(tab1, text="K.A.T.T.Z. web scraper").grid(row=0, column= 0, padx = 10, pady=10)
    jobTitleEntry = Label(tab1, text="Job title").grid(row=1, sticky=W, padx = 10, pady=10)
    entry1 = Entry(tab1).grid(row=1, column=1, padx = 10, pady=10)
    stateEntry = Label(tab1, text="State").grid(row=2, sticky=W, padx = 10, pady=10)
    entry2 = Entry(tab1).grid(row=2, column=1,padx = 10, pady=10)
    CityEntry = Label(tab1, text="City").grid(row=3, sticky=W, padx = 10, pady=10)
    entry3 = Entry(tab1).grid(row=3, column=1, padx = 10, pady=10)
    NameOfSearchEntry = Label(tab1, text="Name this search").grid(row=4, sticky=W, padx = 10, pady=10)
    entry4 = Entry(tab1).grid(row=4, column=1, padx = 10, pady=10)
    searchButton = Button(tab1, text="Search Indeed.com").grid(row=5, padx = 10, pady=10)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    tab2 = Tab(root, "Results")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    tab3 = Tab(root, "Analytics")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    tab4 = Tab(root, "Export/Import")
    #Option menu for saved search
    savedSearch = StringVar(tab4)
    savedSearch.set("choose a saved search") #default saved search
    savedSearchOption = OptionMenu(tab4, savedSearch, "choose a saved search", "two")
    savedSearchOption.grid(row=0, column= 0, padx = 5, pady=5)

    #
    renameSearch = Label(tab4, text="Rename Search: ").grid(row=1, sticky=W, padx = 5, pady=5)
    entry1 = Entry(tab4).grid(row=1, column=1, padx = 5, pady=5)
    searchExtension = StringVar(tab4)
    searchExtension.set("choose a file extension") #default
    searchExtensionOption = OptionMenu(tab4, searchExtension, "choose a file extension", ".pdf", ".jpeg", ".?others?")
    searchExtensionOption.grid(row=1, column= 2, padx = 5, pady=5)
    exportDestination = Label(tab4, text="Export Destination").grid(row=2, sticky=W, padx = 5, pady=5)
    entry2 = Entry(tab4).grid(row=2, column=1,padx = 5, pady=5)
    entry2Button = Button(tab4, text="Choose location").grid(row=2, column=2,padx = 5, pady=5, command=GUIFunctions.chooseExportLocation(tab4, entry2))




    importDestination = Label(tab4, text="Import Destination").grid(row=3, sticky=W, padx = 5, pady=5)
    entry3 = Entry(tab4).grid(row=3, column=1, padx = 5, pady=5)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    tab5 = Tab(root, "About")



    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    bar.add(tab1)  # add the tabs to the tab bar
    bar.add(tab2)
    bar.add(tab3)
    bar.add(tab4)
    bar.add(tab5)

    bar.config(bd=2, relief=RIDGE)			# add some border

    bar.show()
    root.mainloop()