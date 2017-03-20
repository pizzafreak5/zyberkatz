# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tegan Straley
# Port scanner in python
# created for CSCI 4800, cyber security programming
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# file: GUIFunctions.py
# Creates the back-end side of a port scanner with Python's tkinter libraries.
# portScan() - uses code from lab02 to port scan from and to a specified port. Has input validation at beginning.
# NewFile() - Erases the text in all the boxes of the GUI.
# AboutAuthor() - displays out information about me (Tegan Straley)
# AboutPortScanner() - displays out information about port scanning :)

from tkinter import *
from tkinter import filedialog
import socket
from tkinter import messagebox
import sys
import GUIFrame



def NewSearch():
    GUIFrame.entry1.delete(0, END)
    GUIFrame.entry2.delete(0, END)
    GUIFrame.entry3.delete(0, END)
    GUIFrame.listbox.delete(0, END)


def AboutAuthor():
    print("Created by: Tegan Straley\nClass: CSCI 4800\nFebruary 28, 2017\n")
    GUIFrame.listbox.delete(0, END)
    GUIFrame.listbox.insert(END, "Author: Tegan Straley\n\n")
    GUIFrame.listbox.insert(END, "Class: CSCI 4800")
    GUIFrame.listbox.insert(END, "Date: February 28, 2017")


def chooseExportLocation(outputTab, output):
    outputTab.output = filedialog.askopenfilename(initialdir="/", title="select file",
                                                  filetypes=(("jpeg files", "*jpg"), ("all files", "*.*")))

