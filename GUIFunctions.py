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
import tkinter as tk
import socket
import threading
import search_logic
from tkinter import messagebox
import sys
import datetime
################try matplotlib or tk.Canvas to create graphs


aboutTxt = """
Katz Attack Triple Threat Z'craper: (KATTZ)
Licensed 2017, March 25th.

Release version # 1.0.4

This web scrapper was designed to scrape and search Indeed.com
for a specified job and/or location, then storing the information
in a SQL database. It will be possible to look up analytics for the job
searches as well as comparative analytics on many of the job searches. 

Powered by open-source software
"""

disclaimer = """
Disclaimer

This tool was manufactured for an university class project. Much testing
has been performed, however unforeseen scenarios may impose undesirable
output and/or operation. There is no warranty to the output and/or operation
provided by this tool. This tool should be considered as a learning tool
and not be applied for professional applications.

Thank you,
Justin Hockenberry, Gediminas Jakstonis,
Garrett Schwartz, & Tegan Straley\n"""



def about():
    # About option from drop down window
    # Opens new window to display About message and Disclaimer
    toplevel = Toplevel()
    toplevel.iconbitmap('sideprofileCat.ico')
    label1 = Label(toplevel, text=aboutTxt, height=0, width=60)
    label1.pack()
    label2 = Label(toplevel, text=disclaimer, height=0, width=60)
    label2.pack()




def play(self):
    # self.updateStatus("Please wait, scanning remote host...")
    try:
        # Check if valid IP address, if not valid Catch Exception

        # If the Starting and Ending Ports are valid and If Starting is smaller than Ending Port
        if self.entry1.get() and self.entry2.get() and self.entry3.get():
            # If not already running start a new thread to scan
            if self.isRunning == False:
                self.isRunning = True
                self.scanThread = threading.Thread(target=self.run)
                self.scanThread.start()
        else:
            self.isRunning = False
            self.stop()
    except ValueError:
        self.isRunning = False
        self.stop()



def run(self):

    try:
        for port in range(int(self.entry2.get()), int(self.entry3.get())):

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

    except socket.error:
        self.updateStatus("Couldn't connect to server")




def output(self):
    # Don't try to save while a scan is ongoing
    # if self.isRunning == False:
    try:
        self.root.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        # Write to output file
        with open(self.root.filename, 'w') as f:
            f.write("-" * 35)


        self.updateStatus("Output file created: {}".format(self.filename))

    except FileNotFoundError:
        self.updateStatus("No such file or directory selected...")
        # else:
        #       self.updateStatus("Can't save output while running...")

def newSearch(jobTitle, location, searchTitle):
    search_logic.run_search(jobTitle, location, searchTitle)



def returnResults(search):
    print(search)


def createPieChart(search,graph,category):
    print(search)
    print(graph)
    print(category)

    # Data Collection for Pie Chart for Job Experience Category
    #
    # new_job_exp_info = [0, 0, 0]  # each job exp is a index value
    # state = "CO"  # casual variable
    #
    # for row in db_cursor.execute('SELECT job_exp FROM search WHERE job_loc LIKE "%' + state + '%"'):
    #
    #     row_info = []
    #     for i in range(len(row)):
    #         if (row[i] == 'entry_level'):
    #             temp = new_job_exp_info[0]
    #             new_job_exp_info[0] = temp + 1
    #         elif (row[i] == 'mid_level'):
    #             temp = new_job_exp_info[1]
    #             new_job_exp_info[1] = temp + 1
    #         elif (row[i] == 'senior_level'):
    #             temp = new_job_exp_info[2]
    #             new_job_exp_info[2] = temp + 1
    #
    # print(new_job_exp_info)

    # Data Collection for Pie Chart for Job Type Category
    #
    # new_job_type_info = [0, 0, 0, 0, 0, 0]  # each job type is a index value
    # state = "CO"  # casual variable
    #
    # for row in db_cursor.execute('SELECT job_type FROM search WHERE job_loc LIKE "%' + state + '%"'):
    #
    #     row_info = []
    #     for i in range(len(row)):
    #         if (row[i] == 'fulltime'):
    #             temp = new_job_type_info[0]
    #             new_job_exp_info[0] = temp + 1
    #         elif (row[i] == 'contract'):
    #             temp = new_job_type_info[1]
    #             new_job_exp_info[1] = temp + 1
    #         elif (row[i] == 'internship'):
    #             temp = new_job_type_info[2]
    #             new_job_exp_info[2] = temp + 1
    #         elif (row[i] == 'temporary'):
    #             temp = new_job_type_info[3]
    #             new_job_exp_info[3] = temp + 1
    #         elif (row[i] == 'parttime'):
    #             temp = new_job_type_info[4]
    #             new_job_exp_info[4] = temp + 1
    #         elif (row[i] == 'commission'):
    #             temp = new_job_type_info[5]
    #             new_job_exp_info[5] = temp + 1
    #
    # print(new_job_type_info)
    #########################################################

    # Pie Chart for Job Experience Category
    #
    # job_exp = ['entry_level', 'mid_level', 'senior_level']
    # slices02 = [7, 2, 13]
    # plt.pie(slices02,
    #         labels=job_exp,
    #         startangle=90,
    #         shadow=True,
    #         explode=(0, 0.1, 0),
    #         autopct='%1.1f%%')
    # plt.title('job_exp Pie Graph\nCheck it out')
    # plt.legend()
    # plt.show()

    # Pie Chart for Job Type Category
    #
    # job_types = ['fulltime', 'contract', 'internship', 'temporary',
    #              'parttime', 'commission']
    # slices01 = [7,2,13,34,40,10]
    # plt.pie(slices01,
    #         labels=job_types,
    #         startangle=90,
    #         shadow=True,
    #         explode=(0,0.1,0,0,0,0),
    #         autopct= '%1.1f%%')
    # plt.title('job_types Pie Graph\nCheck it out')
    # plt.legend()
    # plt.show()
