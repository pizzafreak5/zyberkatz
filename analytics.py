import scraper
import sqlite3
import json
import scraper
import search
import db
import sqlite3
from collections import OrderedDict
import tkinter as tk
from tkinter import Tk, Label, Button
import webbrowser
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")  # Needed so that tkinter doesn't crash
from matplotlib import pyplot as plt
import numpy as np





def resultsChart(searchTitle):


    datab = sqlite3.connect(db.information['zyber.db'])
    db_cursor = datab.cursor()

    #Show the entries in the database
    column_names_short = [
                    'Company',
                    'Job title',
                    'Location'
                    ]
    #Dont use --->sqlCellData = []    # each index (list of a list)
    sql_info = []       # each job is a index value
    #sql_info = np.sql_info([['','']])
    row_info = ['Company',
                'Job title',
                'Location',
                'Salary',
                'Web Links']
    rowNumber = 1
    for row in db_cursor.execute('SELECT company, job_title, job_loc, salary_est, link FROM listings')# WHERE job_loc LIKE "%'+state+'%"'):
        print ('ENTRY:\n**********************************************************')

        #row_info = np.row_info([])
        for i in range(len(row)):
            #print (column_names_short[i] + ':' + row[i])
            #tempString = column_names_short[i] + ':' + row[i] + "\n"
            #Dont use --->sqlCellData.append(row[i])
            #row_info.insert(0, row[i])
            row_info.append(row[i])
            print (row_info)
        #sql_info.append(row_info)
        #sql_info.append([[row,row_info]])
        print('**********************************************************\n')
        rowNumber+=1
    #print(sql_info[0])
    print(rowNumber," entries found")

    # for row in range(len(sql_info)):
    #     for column in range(len(sql_info[row])):
    #         print(sql_info[row][column], end=" - ")
    #     print("*************************************")

    #for i in range(len(sqlCellData)):
    #    print (sqlCellData[i])
    # #Show the entries in the database
    # for row in db_cursor.execute('SELECT job_loc FROM listings WHERE job_loc LIKE "%'+city+'%"'):
    #     print ('ENTRY:\n**********************************************************')
    #     for i in range(len(row)):
    #         print (column_names[i] + ':' + row[i])
    #     print('**********************************************************\n')
    #salary_est
    #Show the entries in the database
    # for row in db_cursor.execute('SELECT salary_est FROM listings WHERE job_loc LIKE "%CO%"'):
    #     print ('ENTRY:\n**********************************************************')
    #     for i in range(len(row)):
    #         print (column_names[i] + ':' + row[i])
    #     print('**********************************************************\n')
    #
    # #Show the entries in the database
    # for row in db_cursor.execute('SELECT job_loc FROM listings WHERE job_loc LIKE "%CO%"'):
    #     print ('ENTRY:\n**********************************************************')
    #     for i in range(len(row)):
    #         print (column_names[i] + ':' + row[i])
    #     print('**********************************************************\n')
    #
    # #Show the entries in the database
    # for row in db_cursor.execute('SELECT * FROM listings WHERE company LIKE "Ver%"'):
    #     print ('ENTRY:\n**********************************************************')
    #     for i in range(len(row)):
    #         print (column_names[i] + ':' + row[i])
    #     print('**********************************************************\n')
    #
    # #Show the Company and Job Title entries
    # for row in db_cursor.execute('SELECT company, job_title FROM listings'):
    #     print ('ENTRY:\n**********************************************************')
    #     for i in range(len(row)):
    #         print (column_names[i] + ':' + row[i])
    #     print('**********************************************************\n')
    #
    # #Show the entries in the database
    # for row in db_cursor.execute('SELECT * FROM listings WHERE company = "Verizon"'):
    #     print ('ENTRY:\n**********************************************************')
    #     for i in range(len(row)):
    #         print (column_names[i] + ':' + row[i])
    #     print('**********************************************************\n')
    #
    #Show the entries in the database
    # for row in db_cursor.execute('SELECT * FROM listings'):
    #     print ('ENTRY:\n**********************************************************')
    #     for i in range(len(row)):
    #         print (column_names[i] + ':' + row[i])
    #     print('**********************************************************\n')





class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, rowNumber,5)
        t.pack(side="top", fill="x")


class SimpleTable(tk.Frame):
    #def callback(event):
    #    webbrowser.open_new(r"http://www.indeed.com")

    def callback(self, event, link):
        print(link)
        webbrowser.open_new(link)

    def callback1(self, event):
        webbrowser.open_new(event.widget.cget("text"))

    def __init__(self, parent, rows=rowNumber, columns=5):


        columnNames = [
            'Company',
            'Job title',
            'Location',
            'Salary',
            'Web Link'
        ]
        # for i in range(columnNames):
        #     row_info.insert(0, columnNames[i])
        # print(row_info)
        # use black background so it "peeks through" to
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        parent.title("Search Results")
        parent.resizable(width=False, height=False)  # Makes user unable to resize window
        self._widgets = []
        self.webLink = ""


        cellCount = 0
########################################################################
        # for row in range(rows):
        #     current_row = []
        #     for column in range(columns):
        #         if (row == 0):
        #            label = tk.Label(self, text="%s/%s" % (columnNames[column], column),
        #                             borderwidth=0, width=20)
        #
        #         label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
        #         current_row.append(label)
        #         cellCount = cellCount+1
        #     self._widgets.append(current_row)
        #
        # for column in range(columns):
        #     self.grid_columnconfigure(column, weight=1)
        # cellCount = 0
########################################################################
        for row in range(rows):
            current_row = []
            for column in range(columns):

                #if (row == 0):
                #    label = tk.Label(self, text="%s/%s" % (columnNames[column], column),
                #                     borderwidth=0, width=20)
                if (column == 4 and row != 0):
                     link = row_info[cellCount]

                     label = tk.Label(self, text="Job Posting", fg="blue", cursor="hand2",
                                                    borderwidth = 0)#, width = 10)
                     label.bind("<Button-1>", lambda event, arg=link: self.callback(event, arg))

                else:
                    #label = tk.Label(self, text="%s/%s" % (row_info[cellCount], column),
                    label = tk.Label(self, text="%s" % (row_info[cellCount]),
                                     borderwidth=0)#, width=20)
                if (row == 0):
                    label.configure(background='grey')

                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
                cellCount = cellCount+1
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
# class GUI(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#
#         self.score = 0
#
#         self.buttonDic = {
#         'Brown Rice':0,
#         'Banzai Veg':0,
#         'Red Cabbage':0,
#         'Black Beans':0
#         }
#
#         aFrame = self.aFrame = tk.Frame(self)
#         aFrame.grid()
#
#         for key in self.buttonDic:
#             self.buttonDic[key] = tk.IntVar()
#             aCheckButton = tk.Checkbutton(aFrame, text=key,
#                                             variable=self.buttonDic[key])
#             aCheckButton.grid(sticky='w')
#
#         submitButton = tk.Button(aFrame, text="Submit",
#                                         command=self.query_checkbuttons)
#         submitButton.grid()
#
#         self.trueList = ['Brown Rice', 'Black Beans']
#
#     def query_checkbuttons(self):
#         for key, value in self.buttonDic.items():
#             state = value.get()
#             if state != 0:
#                 if key in self.trueList:
#                     self.score += 1
#                 else:
#                     self.score -= 1
#                 self.buttonDic[key].set(0)
#         self.result_screen()
#
#     def result_screen(self):
#         self.aFrame.grid_forget()
#         self.rFrame = tk.Frame(self)
#         self.rFrame.grid()
#         self.scoreText = tk.Text(self.rFrame, width=200, height=50)
#         self.scoreText.grid()
#         self.scoreText.insert('end', printOutString)
#         self.after(3000, func=self.go_back)
#
#     def go_back(self):
#         self.score = 0
#         self.rFrame.destroy()
#         self.aFrame.grid()
#
#
# gui = GUI()
# gui.mainloop()

def analyticsPieChart(jobTitle, category):





def analyticsBarChart(jobTitle, category):





def analyticsHistogram(jobTitle, category):







job_types = ['fulltime', 'contract', 'internship', 'temporary',
             'parttime', 'commission']
slices01 = [7, 2, 13, 34, 40, 10]
plt.pie(slices01,
        labels=job_types,
        startangle=90,
        shadow=True,
        explode=(0, 1, 0, 0, 0, 0),
        autopct='%1.1f%%')
plt.title('job_types Graph\nCheck it out')
plt.legend()
plt.show()
#
# job_exp = ['entry_level', 'mid_level', 'senior_level']
# slices02 = [7,2,13]
# plt.pie(slices02,
#         labels=job_exp,
#         startangle=90,
#         shadow=True,
#         explode=(0,0.1,0),
#         autopct= '%1.1f%%')
# plt.title('job_exp Graph\nCheck it out')
# plt.legend()
# plt.show()




# How to Pie Chart
# slices = [7,2,2,13]
# activities = ['sleeping', 'eating', 'working', 'playing']
#
# plt.pie(slices,
#         labels=activities,
#         startangle=90,
#         shadow=True,
#         explode=(0,0.1,0,0),
#         autopct= '%1.1f%%')
#
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()


# How to Histogram
# population_ages = [22,55,62,45,21,22,34,42,42,4,88,99,102,110,130,121,122,130,111,115,112,80,75,65,54,44,43,42,48]
#
# bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130]
#
# plt.hist(population_ages, bins, histtype='bar', rwidth= 0.8)
#
# plt.xlabel('x - axis')
# plt.ylabel('y - axis')
# plt.title('Interesting Graph\nCheck it out')
# plt.show()


# How to Bar chart
# x = [2,4,6,8,10]
# y = [6,7,8,2,4]
# x2 = [1,3,5,7,9]
# y2 = [7,8,2,4,2]
#
# plt.bar(x,y,label= 'Bar one')
# plt.bar(x2,y2, label = 'Bar two')
#
# plt.xlabel('x - axis')
# plt.ylabel('y - axis')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()


# How to Line Chart
# x = [1,2,3]
# y = [5,7,4]
# x2 = [1,2,3]
# y2 = [10,14,12]
#
# plt.plot(x,y, label='first line')
# plt.plot(x2,y2, label = 'second line')
# plt.xlabel('Plot Number')
# plt.ylabel('Important var')
# plt.title('Interesting graph\nCheck it out')
# plt.legend()
# plt.show()







# Usages Examples

# '''generate url

file = open('url.json', 'r')  # open the json file
url_dict = json.load(file)  # load it in as a dictionary
url = scraper.generate_url(url_dict)  # use the dictionary to assemble a url
print(url)  # show the url
# '''

###################################
#######DATABASE AND SCRAPING#######
###################################
# Preparing the sqlite3 database for scraper.py
listings = sqlite3.connect(':memory:')  # Create a database in ram
# Change :memory: to a different value to not be in ram
db_cursor = listings.cursor()  # Create a cursor that will be passed into scraper.py
# Create the table that will be used by scraper.py
db_cursor.execute('''
CREATE TABLE listings
(
hash_val         TEXT PRIMARY KEY NOT NULL,
company          TEXT,
time_posted      TEXT,
job_title        TEXT,
job_desc         TEXT,
job_loc          TEXT,
job_exp          TEXT,
salary_est       TEXT,
job_type         TEXT,
link             TEXT,
job_text         TEXT
);
''')
listings.commit()  # updates SQL database

# dict for settings that is passed to a scraper object
settings = {
    'website_url': 'http://www.indeed.com/jobs?q=Computer+Science',  # &l=Denver%2C+CO',
    'div_class_links': 'pagination',
    'div_class_listings': ['  row  result', 'row  result', 'lastRow  row  result', 'row result', ' row result',
                           ' lastRow row result', 'lastRow row result'],
    'job_type': '',
    'salary_est': '',
    'company_name_tag': 'span',
    'company_name_attrs': {'class': 'company'},
    'time_posted_tag': 'span',
    'time_posted_attrs': {'class': 'date'},
    'job_loc_tag': 'span',
    'job_loc_attrs': {'class': 'location'},
    'job_desc_tag': 'span',
    'job_desc_attrs': {'class': 'summary'},
    'job_title_tag': 'a',
    'limit': 1
}

# '''Create a new scraper object and scrape
# It needs the settings dictionary, the database cursor, and the table name you want to use
scraper1 = scraper.scraper(settings, db_cursor, "listings")
scraper1.scrape(scraper1.url)  # Start it with the initial url provided
# '''

# Save the Entries
listings.commit()

# Names to the respective columns
column_names = ['Hash value',
                'Company',
                'Time posted',
                'Job title',
                'Job description',
                'Location',
                'Experience',
                'Salary estimate',
                'Job type',
                'Job link',
                'Job page text'
                ]

jobType = "Software"
city = "Denver"
state = "CO"
printOutString = ""
tempString = ""

# Show the entries in the database
column_names_short = [
    'Company',
    'Job title',
    'Location'
]
# Dont use --->sqlCellData = []    # each index (list of a list)
sql_info = []  # each job is a index value
# sql_info = np.sql_info([['','']])
row_info = ['Company',
            'Job title',
            'Location',
            'Salary',
            'Web Links']
rowNumber = 1
for row in db_cursor.execute(
        'SELECT company, job_title, job_loc, salary_est, link FROM listings')  # WHERE job_loc LIKE "%'+state+'%"'):
    print('ENTRY:\n**********************************************************')

    # row_info = np.row_info([])
    for i in range(len(row)):
        # print (column_names_short[i] + ':' + row[i])
        # tempString = column_names_short[i] + ':' + row[i] + "\n"
        # Dont use --->sqlCellData.append(row[i])
        # row_info.insert(0, row[i])
        row_info.append(row[i])
        print(row_info)
    # sql_info.append(row_info)
    # sql_info.append([[row,row_info]])
    print('**********************************************************\n')
    rowNumber += 1
# print(sql_info[0])
print(rowNumber, " entries found")


# for row in range(len(sql_info)):
#     for column in range(len(sql_info[row])):
#         print(sql_info[row][column], end=" - ")
#     print("*************************************")

# for i in range(len(sqlCellData)):
#    print (sqlCellData[i])
# #Show the entries in the database
# for row in db_cursor.execute('SELECT job_loc FROM listings WHERE job_loc LIKE "%'+city+'%"'):
#     print ('ENTRY:\n**********************************************************')
#     for i in range(len(row)):
#         print (column_names[i] + ':' + row[i])
#     print('**********************************************************\n')
# salary_est
# Show the entries in the database
# for row in db_cursor.execute('SELECT salary_est FROM listings WHERE job_loc LIKE "%CO%"'):
#     print ('ENTRY:\n**********************************************************')
#     for i in range(len(row)):
#         print (column_names[i] + ':' + row[i])
#     print('**********************************************************\n')
#
# #Show the entries in the database
# for row in db_cursor.execute('SELECT job_loc FROM listings WHERE job_loc LIKE "%CO%"'):
#     print ('ENTRY:\n**********************************************************')
#     for i in range(len(row)):
#         print (column_names[i] + ':' + row[i])
#     print('**********************************************************\n')
#
# #Show the entries in the database
# for row in db_cursor.execute('SELECT * FROM listings WHERE company LIKE "Ver%"'):
#     print ('ENTRY:\n**********************************************************')
#     for i in range(len(row)):
#         print (column_names[i] + ':' + row[i])
#     print('**********************************************************\n')
#
# #Show the Company and Job Title entries
# for row in db_cursor.execute('SELECT company, job_title FROM listings'):
#     print ('ENTRY:\n**********************************************************')
#     for i in range(len(row)):
#         print (column_names[i] + ':' + row[i])
#     print('**********************************************************\n')
#
# #Show the entries in the database
# for row in db_cursor.execute('SELECT * FROM listings WHERE company = "Verizon"'):
#     print ('ENTRY:\n**********************************************************')
#     for i in range(len(row)):
#         print (column_names[i] + ':' + row[i])
#     print('**********************************************************\n')
#
# Show the entries in the database
# for row in db_cursor.execute('SELECT * FROM listings'):
#     print ('ENTRY:\n**********************************************************')
#     for i in range(len(row)):
#         print (column_names[i] + ':' + row[i])
#     print('**********************************************************\n')





class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, rowNumber, 5)
        t.pack(side="top", fill="x")


class SimpleTable(tk.Frame):
    # def callback(event):
    #    webbrowser.open_new(r"http://www.indeed.com")

    def callback(self, event, link):
        print(link)
        webbrowser.open_new(link)

    def callback1(self, event):
        webbrowser.open_new(event.widget.cget("text"))

    def __init__(self, parent, rows=rowNumber, columns=5):

        columnNames = [
            'Company',
            'Job title',
            'Location',
            'Salary',
            'Web Link'
        ]
        # for i in range(columnNames):
        #     row_info.insert(0, columnNames[i])
        # print(row_info)
        # use black background so it "peeks through" to
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        parent.title("Search Results")
        parent.resizable(width=False, height=False)  # Makes user unable to resize window
        self._widgets = []
        self.webLink = ""

        cellCount = 0
        ########################################################################
        # for row in range(rows):
        #     current_row = []
        #     for column in range(columns):
        #         if (row == 0):
        #            label = tk.Label(self, text="%s/%s" % (columnNames[column], column),
        #                             borderwidth=0, width=20)
        #
        #         label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
        #         current_row.append(label)
        #         cellCount = cellCount+1
        #     self._widgets.append(current_row)
        #
        # for column in range(columns):
        #     self.grid_columnconfigure(column, weight=1)
        # cellCount = 0
        ########################################################################
        for row in range(rows):
            current_row = []
            for column in range(columns):

                # if (row == 0):
                #    label = tk.Label(self, text="%s/%s" % (columnNames[column], column),
                #                     borderwidth=0, width=20)
                if (column == 4 and row != 0):
                    link = row_info[cellCount]

                    label = tk.Label(self, text="Job Posting", fg="blue", cursor="hand2",
                                     borderwidth=0)  # , width = 10)
                    label.bind("<Button-1>", lambda event, arg=link: self.callback(event, arg))

                else:
                    # label = tk.Label(self, text="%s/%s" % (row_info[cellCount], column),
                    label = tk.Label(self, text="%s" % (row_info[cellCount]),
                                     borderwidth=0)  # , width=20)
                if (row == 0):
                    label.configure(background='grey')

                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
                cellCount = cellCount + 1
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
# class GUI(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#
#         self.score = 0
#
#         self.buttonDic = {
#         'Brown Rice':0,
#         'Banzai Veg':0,
#         'Red Cabbage':0,
#         'Black Beans':0
#         }
#
#         aFrame = self.aFrame = tk.Frame(self)
#         aFrame.grid()
#
#         for key in self.buttonDic:
#             self.buttonDic[key] = tk.IntVar()
#             aCheckButton = tk.Checkbutton(aFrame, text=key,
#                                             variable=self.buttonDic[key])
#             aCheckButton.grid(sticky='w')
#
#         submitButton = tk.Button(aFrame, text="Submit",
#                                         command=self.query_checkbuttons)
#         submitButton.grid()
#
#         self.trueList = ['Brown Rice', 'Black Beans']
#
#     def query_checkbuttons(self):
#         for key, value in self.buttonDic.items():
#             state = value.get()
#             if state != 0:
#                 if key in self.trueList:
#                     self.score += 1
#                 else:
#                     self.score -= 1
#                 self.buttonDic[key].set(0)
#         self.result_screen()
#
#     def result_screen(self):
#         self.aFrame.grid_forget()
#         self.rFrame = tk.Frame(self)
#         self.rFrame.grid()
#         self.scoreText = tk.Text(self.rFrame, width=200, height=50)
#         self.scoreText.grid()
#         self.scoreText.insert('end', printOutString)
#         self.after(3000, func=self.go_back)
#
#     def go_back(self):
#         self.score = 0
#         self.rFrame.destroy()
#         self.aFrame.grid()
#
#
# gui = GUI()
# gui.mainloop()






