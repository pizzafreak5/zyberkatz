import scraper
import sqlite3
import json
import scraper
import search
import db
import sqlite3
from collections import OrderedDict
import tkinter as tk
from tkinter import Tk, Label, Button, Scrollbar, RIGHT, Y, N, W
import webbrowser
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")  # Needed so that tkinter doesn't crash
from matplotlib import pyplot as plt
import numpy as np


global_db_name = 'zyber.db'
rowNumber = 1
row_info = ['Company',
            'Job title',
            'Location',
            'Salary',
            'Web Links']

class analytic_charts(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # ---------------
        # DB SETUP
        # ---------------
        db = sqlite3.connect(global_db_name)  # Connect to the project database
        db_cursor = db.cursor()

        # Show the entries in the database
        column_names_short = [
            'Company',
            'Job title',
            'Location'
        ]
        sql_info = []  # each job is a index value

        # row_info = ['Company',
        #             'Job title',
        #             'Location',
        #             'Salary',
        #             'Web Links']
        rowNumber = 1
        for row in db_cursor.execute(
                'SELECT company, job_title, job_loc, salary_est, link FROM listing'):  # WHERE job_loc LIKE "%'+state+'%"'):
            print('ENTRY:\n**********************************************************')

            # ('SELECT company, job_title, job_loc, salary_est, link FROM listing WHERE
            # hash_val IN (SELECT hash_val FROM junction WHERE search_hash IN (SELECT
            # search_hash FROM search WHERE search_title = 'mysearchinthemiddleofthesearch'))

            for i in range(len(row)):
                row_info.append(row[i])
                print(row_info)

            print('**********************************************************\n')
            rowNumber += 1

        print(rowNumber, " entries found")



        t = SimpleTable(self, rowNumber, 5)

        #t.pack(side="top", fill="x")




class SimpleTable(tk.Frame):

    def callback(self, event, link):
        print(link)
        webbrowser.open_new(link)

    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __init__(self, parent, rows=rowNumber, columns=5):

        self.canvas = tk.Canvas(parent, borderwidth=10, background="grey", height = 15, width = 1066)
        tk.Frame.__init__(self, self.canvas)




        columnNames = [
            'Company',
            'Job title',
            'Location',
            'Salary',
            'Web Link'
        ]

        #tk.Frame.__init__(self, parent, background="grey")
        parent.title("Search Results")
       # parent.resizable(width=False, height=False)  # Makes user unable to resize window

        self._widgets = []
        self.webLink = ""

        cellCount = 0

        for row in range(rows):
            current_row = []
            for column in range(columns):

                #if (row == 0):
                #    label = tk.Label(self, text="%s/%s" % (columnNames[column], column),
                #                     borderwidth=0, width=20)
                if (column == 4 and row != 0):
                     link = row_info[cellCount]

                     label = tk.Label(self, text="Job Posting", fg="blue", cursor="hand2")#,
                                                    #borderwidth = 0)#, width = 10)
                     label.bind("<Button-1>", lambda event, arg=link: self.callback(event, arg))

                else:
                    label = tk.Label(self, text="%s" % (row_info[cellCount]))#,
                                     #borderwidth=0)#, width=20)
                if (row == 0):
                    label.configure(background='grey')

                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
                cellCount = cellCount+1
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

        self.vsb = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        # self.vsb01 = tk.Scrollbar(parent, orient="horizontal", command=self.canvas.xview)
        # self.canvas.configure(xscrollcommand=self.vsb01.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0,0), window=self, anchor=N+W)
        self.bind("<Configure>", self.OnFrameConfigure)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


        # Attach Scrollbar to Listbox
        # scrollbar = Scrollbar(parent)
        # scrollbar.pack(side=RIGHT, fill=Y)
        # parent.config(yscrollcommand=scrollbar.set)
        # scrollbar.config(command=parent.yview)



if __name__ == "__main__":
    app = analytic_charts()
    app.mainloop()


def analyticsPieChart(jobTitle, category):
    print("")




def analyticsBarChart(jobTitle, category):
    print("")




def analyticsHistogram(jobTitle, category):
    print("")






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





