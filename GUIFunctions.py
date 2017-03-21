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



def play(self):

    self.updateStatus("Please wait, scanning remote host...")

    try:
        # Check if valid IP address, if not valid Catch Exception
        network = ipaddress.IPv4Network(self.e1.get())

        # If the Starting and Ending Ports are valid and If Starting is smaller than Ending Port
        if self.e2.get().isdigit() and self.e3.get().isdigit() and self.e2.get() < self.e3.get():
            # If not already running start a new thread to scan
            if self.isRunning == False:
                self.isRunning = True
                self.scanThread = threading.Thread(target=self.run)
                self.scanThread.start()
        else:
            self.isRunning = False
            self.updateStatus("Bad input...")
            self.stop()
    except ValueError:
        self.isRunning = False
        self.updateStatus("Address is invalid for IPv4")
        self.stop()


def run(self):

    # Clear output 'listbox' and start fresh
    self.foundOpenList = []
    self.listbox.delete(0, END)

    try:
        for port in range(int(self.e2.get()), int(self.e3.get())):

            # Interrupt if user clicks Stop Button
            if self.isRunning == True:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                sock.settimeout(.5)
                sock.setblocking(1)

                result = sock.connect_ex((self.e1.get(), port))
                if result == 0:
                    # Store open ports for potential output file
                    self.foundOpenList.append(" Port {}: 	 Open".format(port))
                    # Print-out to on-screen listbox
                    self.listbox.insert(END, " Port {}: 	 Open".format(port))
                sock.close()

        # When successfully completed without interrupt
        if self.isRunning == True:
            self.updateStatus("Scan Complete...")
            try:
                # Stops the extra thread we used to scan
                self.isRunning = False
                self.scanThread.join(0)
                self.scanThread = None
            except (AttributeError, RuntimeError):  # Scan thread could be None
                pass

    except socket.gaierror:
        self.updateStatus("Hostname could not be resolved. Stopping...")
    except socket.error:
        self.updateStatus("Couldn't connect to server")




def output(self):

    # Don't try to save while a scan is ongoing
    if self.isRunning == False:
        try:
            root.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                         filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            # Write to output file
            with open(root.filename, 'w') as f:
                f.write("-" * 35)
                f.write('\n---- Foxy Port Scanner Output -----\n\n')
                f.write('Remote Host IP: {}\n'.format(self.e1.get()))
                f.write("Starting Port: {}\n".format(self.e2.get()))
                f.write("Ending Port: {}\n".format(self.e3.get()))
                f.write('\nTimestamp: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()))
                f.write("-" * 35 + "\n")
                f.write('\n'.join(self.foundOpenList))

            self.updateStatus("Output file created: {}".format(root.filename))

        except FileNotFoundError:
            self.updateStatus("No such file or directory selected...")
    else:
            self.updateStatus("Can't save output while running...")