
import sqlite3
import tkinter as tk
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")  # Needed so that tkinter doesn't crash
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import numpy.ma
import matplotlib.pyplot as plt

# Font size for the title
LARGE_FONT = ("fixedsys", 18)
SMALL_FONT = ("arial", 7)
BUTTON_FONT = ("arial", 14)

import analytics_chart

global_db_name = 'zyber.db'
rowNumber = 1
row_info = ['Company',
            'Job title',
            'Location',
            'Salary',
            'Web Links']

class analyticsGUI(tk.Tk):
    def __init__(self, searchJobTitle):
        self.searchJobTitle= searchJobTitle
        self.analyticsPage()



    def analyticsPage(self):

        self.analyticsWindow = tk.Toplevel(background = 'grey')
        self.analyticsWindow.wm_title("Analytics")
        self.analyticsWindow.wm_geometry("300x200")
        #self.analyticsWindow.resizable(0, 0)

        # ****** Top  Toolbar ********
        self.toolbar = Frame(self.analyticsWindow, background = 'grey')

        # ****** Top Button Toolbar ********
        self.resultsButton = Button(self.toolbar, text="Results Chart", command=self.goResultsChart,
                                    highlightbackground='grey', height=1, width =20).grid(row=0, column=2,  pady=2)


        self.toolbar.pack(side=TOP, fill=Y)  # Adds toolbar to frame

        # ****** Main Input Frame *******
        self.jobExpRadio = IntVar()
        self.jobTitleRadio = IntVar()
        self.salaryEstRadio = IntVar()

        self.frame = Frame(self.analyticsWindow,background = 'grey')

        self.salaryEst = Label(self.frame, text="Salary Estimates:", background='grey').grid(row=1, column=1)
        pie01 = Radiobutton(self.frame, text="Pie Chart", background='grey',
                            variable=self.salaryEstRadio, value=1).grid(row=1, column=2, sticky=W)
        bar01 = Radiobutton(self.frame, text="Bar Graph", background='grey',
                            variable=self.salaryEstRadio, value=2).grid(row=2, column=2, sticky=W)

        goButton01 = Button(self.frame, text="Go", highlightbackground='green', width=5,
                            command=self.selectedSalaryEstGo).grid(row=1, column=3)


        self.jobExp = Label(self.frame, text="Job Experience:", background = 'grey').grid(row=3, column=1)
        pie02 = Radiobutton(self.frame, text="Pie Chart", background = 'grey',
                            variable=self.jobExpRadio, value=3).grid(row=3, column=2, sticky=W)
        bar02 = Radiobutton(self.frame, text="Bar Graph", background = 'grey',
                            variable=self.jobExpRadio, value=4).grid(row=4, column=2, sticky=W)

        goButton02 = Button(self.frame, text="Go", highlightbackground='green', width =5,
                            command=self.selectedJobExpGo).grid(row=3, column=3)

        self.jobType = Label(self.frame, text="Job Type:", background = 'grey').grid(row=5, column=1)
        pie03 = Radiobutton(self.frame, text="Pie Chart", background = 'grey',
                            variable=self.jobTitleRadio, value=5).grid(row=5, column=2, sticky=W)
        bar03 = Radiobutton(self.frame, text="Bar Graph", background = 'grey',
                            variable=self.jobTitleRadio, value=6).grid(row=6, column=2, sticky=W)

        goButton03 = Button(self.frame, text="Go", highlightbackground='green', width =5,
                            command=self.selectedJobTypeGo).grid(row=5, column=3)

        self.frame.pack()


    def goResultsChart(self):
        searchJobTitle = self.searchJobTitle
        tmp = analytics_chart.ResultsChart(searchJobTitle)
    def doNothing(self):
        print("")

    def selectedSalaryEstGo(self):
        #print("variable is", self.salaryEstRadio.get())

        if (self.salaryEstRadio.get() == 1):

            self.analyticsSalaryPieChart()
        elif (self.salaryEstRadio.get() == 2):

            self.analyticsSalaryBarChart()
        else:
            self.doNothing()

    def selectedJobExpGo(self):
        #print("variable is", self.jobExpRadio.get())

        if (self.jobExpRadio.get() == 3):

            self.analyticsJobExpPieChart()

        elif (self.jobExpRadio.get() == 4):

            self.analyticsJobExpBarChart()
        else:
            self.doNothing()

    def selectedJobTypeGo(self):
        #print("variable is", self.jobTitleRadio.get())

        if (self.jobTitleRadio.get() == 5):

            self.analyticsJobTypePieChart()
        elif (self.jobTitleRadio.get() == 6):

            self.analyticsJobTypeBarChart()
        else:
            self.doNothing()

    def analyticsJobTypePieChart(self):
        # ---------------
        # DB SETUP
        # ---------------
        db = sqlite3.connect(global_db_name)  # Connect to the project database
        db_cursor = db.cursor()

        # Prep to find the searches
        search_list = "'"
        # For singular it is done inside the query string itself
        search_list += "' or search_title = '".join(self.searchJobTitle)
        search_list += "'"

        jobTypesNumbersList = [0,0,0,0,0,0]

        # Query
        query = '''
                SELECT job_type
                from listing
                where hash_val
                in
                (
                select hash_val
                from junction
                where search_hash
                in
                (
                select search_hash
                from search
                where search_title = {}));
                '''.format(search_list)

        for row in db_cursor.execute(query):

            for i in range(len(row)):
                if (row[i] == 'fulltime'):
                    temp = jobTypesNumbersList[0]
                    temp = temp+1
                    jobTypesNumbersList[0] = temp
                elif (row[i] == 'contract'):
                    temp = jobTypesNumbersList[1]
                    temp = temp + 1
                    jobTypesNumbersList[1] = temp
                elif (row[i] == 'internship'):
                    temp = jobTypesNumbersList[2]
                    temp = temp + 1
                    jobTypesNumbersList[2] = temp
                elif (row[i] == 'temporary'):
                    temp = jobTypesNumbersList[3]
                    temp = temp + 1
                    jobTypesNumbersList[3] = temp
                elif (row[i] == 'parttime'):
                    temp = jobTypesNumbersList[4]
                    temp = temp + 1
                    jobTypesNumbersList[4] = temp
                elif (row[i] == 'commission'):
                    temp = jobTypesNumbersList[5]
                    temp = temp + 1
                    jobTypesNumbersList[5] = temp
                #print(row[i])

        #print(jobTypesNumbersList)

        job_types = ['fulltime', 'contract', 'internship', 'temporary',
                     'parttime', 'commission']
        plt.pie(jobTypesNumbersList,
                labels=job_types,
                #startangle=90,
                shadow=True,
                explode=(0,0,0,0,0,0),
                autopct='%1.1f%%')
        plt.title('{0} Job Types Graph'.format(search_list))
        plt.legend()
        plt.show()

    def analyticsJobTypeBarChart(self):
        # ---------------
        # DB SETUP
        # ---------------
        db = sqlite3.connect(global_db_name)  # Connect to the project database
        db_cursor = db.cursor()

        # Prep to find the searches
        search_list = "'"
        # For singular it is done inside the query string itself
        search_list += "' or search_title = '".join(self.searchJobTitle)
        search_list += "'"

        jobTypesNumbersList = [0, 0, 0, 0, 0, 0]

        # Query
        query = '''
                SELECT job_type
                from listing
                where hash_val
                in
                (
                select hash_val
                from junction
                where search_hash
                in
                (
                select search_hash
                from search
                where search_title = {}));
                '''.format(search_list)

        for row in db_cursor.execute(query):

            for i in range(len(row)):
                if (row[i] == 'fulltime'):
                    temp = jobTypesNumbersList[0]
                    temp = temp + 1
                    jobTypesNumbersList[0] = temp
                elif (row[i] == 'contract'):
                    temp = jobTypesNumbersList[1]
                    temp = temp + 1
                    jobTypesNumbersList[1] = temp
                elif (row[i] == 'internship'):
                    temp = jobTypesNumbersList[2]
                    temp = temp + 1
                    jobTypesNumbersList[2] = temp
                elif (row[i] == 'temporary'):
                    temp = jobTypesNumbersList[3]
                    temp = temp + 1
                    jobTypesNumbersList[3] = temp
                elif (row[i] == 'parttime'):
                    temp = jobTypesNumbersList[4]
                    temp = temp + 1
                    jobTypesNumbersList[4] = temp
                elif (row[i] == 'commission'):
                    temp = jobTypesNumbersList[5]
                    temp = temp + 1
                    jobTypesNumbersList[5] = temp
                #print(row[i])

        #print(jobTypesNumbersList)

        objects = ('fulltime', 'contract', 'internship', 'temporary',
                     'parttime', 'commission')
        y_pos = np.arange(len(objects))

        plt.bar(y_pos, jobTypesNumbersList, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.xlabel('Job Types')
        plt.ylabel('Number of Types')
        plt.title('{0} Job Types Graph'.format(search_list))

        plt.show()

    def analyticsJobExpPieChart(self):

        # ---------------
        # DB SETUP
        # ---------------
        db = sqlite3.connect(global_db_name)  # Connect to the project database
        db_cursor = db.cursor()

        # Prep to find the searches
        search_list = "'"
        # For singular it is done inside the query string itself
        search_list += "' or search_title = '".join(self.searchJobTitle)
        search_list += "'"

        jobExpNumbersList = [0, 0, 0,]

        # Query
        query = '''
               SELECT job_exp
               from listing
               where hash_val
               in
               (
               select hash_val
               from junction
               where search_hash
               in
               (
               select search_hash
               from search
               where search_title = {}));
               '''.format(search_list)

        for row in db_cursor.execute(query):

            for i in range(len(row)):
                if (row[i] == 'entry_level'):
                    temp = jobExpNumbersList[0]
                    temp = temp + 1
                    jobExpNumbersList[0] = temp
                elif (row[i] == 'mid_level'):
                    temp = jobExpNumbersList[1]
                    temp = temp + 1
                    jobExpNumbersList[1] = temp
                elif (row[i] == 'senior_level'):
                    temp = jobExpNumbersList[2]
                    temp = temp + 1
                    jobExpNumbersList[2] = temp
                #print(row[i])

        #print(jobExpNumbersList)

        job_exp = ['entry_level', 'mid_level', 'senior_level']

        plt.pie(jobExpNumbersList,
                labels=job_exp,
                #startangle=90,
                shadow=True,
                explode=(0,0,0),
                autopct= '%1.1f%%')
        plt.title('{0} Job Experience Graph'.format(search_list))
        plt.legend()
        plt.show()

    def analyticsJobExpBarChart(self):

        # ---------------
        # DB SETUP
        # ---------------
        db = sqlite3.connect(global_db_name)  # Connect to the project database
        db_cursor = db.cursor()

        # Prep to find the searches
        search_list = "'"
        # For singular it is done inside the query string itself
        search_list += "' or search_title = '".join(self.searchJobTitle)
        search_list += "'"

        jobExpNumbersList = [0, 0, 0]

        # Query
        query = '''
              SELECT job_exp
              from listing
              where hash_val
              in
              (
              select hash_val
              from junction
              where search_hash
              in
              (
              select search_hash
              from search
              where search_title = {}));
              '''.format(search_list)

        for row in db_cursor.execute(query):

            for i in range(len(row)):
                if (row[i] == 'entry_level'):
                    temp = jobExpNumbersList[0]
                    temp = temp + 1
                    jobExpNumbersList[0] = temp
                elif (row[i] == 'mid_level'):
                    temp = jobExpNumbersList[1]
                    temp = temp + 1
                    jobExpNumbersList[1] = temp
                elif (row[i] == 'senior_level'):
                    temp = jobExpNumbersList[2]
                    temp = temp + 1
                    jobExpNumbersList[2] = temp
                #print(row[i])

        #print(jobExpNumbersList)


        objects = ('entry_level', 'mid_level', 'senior_level')
        y_pos = np.arange(len(objects))

        plt.bar(y_pos, jobExpNumbersList, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.xlabel('Types of Experience')
        plt.ylabel('Level of Experience')
        plt.title('{0} Job Experience Graph'.format(search_list))

        plt.show()



    def analyticsSalaryPieChart(self):

        # ---------------
        # DB SETUP
        # ---------------
        db = sqlite3.connect(global_db_name)  # Connect to the project database
        db_cursor = db.cursor()

        # Prep to find the searches
        search_list = "'"
        # For singular it is done inside the query string itself
        search_list += "' or search_title = '".join(self.searchJobTitle)
        search_list += "'"

        salaryEstNumbersList = [0, 0, 0, 0, 0]

        # Query
        query = '''
              SELECT salary_est
              from listing
              where hash_val
              in
              (
              select hash_val
              from junction
              where search_hash
              in
              (
              select search_hash
              from search
              where search_title = {}));
              '''.format(search_list)

        for row in db_cursor.execute(query):

            for i in range(len(row)):
                if (row[i] == '$14,000'):
                    temp = salaryEstNumbersList[0]
                    temp = temp + 1
                    salaryEstNumbersList[0] = temp
                elif (row[i] == '$30,000'):
                    temp = salaryEstNumbersList[1]
                    temp = temp + 1
                    salaryEstNumbersList[1] = temp
                elif (row[i] == '$50,000'):
                    temp = salaryEstNumbersList[2]
                    temp = temp + 1
                    salaryEstNumbersList[2] = temp
                elif (row[i] == '$70,000'):
                    temp = salaryEstNumbersList[2]
                    temp = temp + 1
                    salaryEstNumbersList[2] = temp
                elif (row[i] == '$90,000'):
                    temp = salaryEstNumbersList[2]
                    temp = temp + 1
                    salaryEstNumbersList[2] = temp
                #print(row[i])

        #print(salaryEstNumbersList)

        salary_est = ['$14,000','$30,000','$50,000','$70,000','$90,000']

        plt.pie(salaryEstNumbersList,
                labels=salary_est,
                #startangle=90,
                shadow=True,
                explode=(0, 0, 0, 0, 0),
                autopct='%1.1f%%')
        plt.title('{0} Salary Estimate Graph'.format(search_list))
        plt.legend()
        plt.show()


    def analyticsSalaryBarChart(self):

        # ---------------
        # DB SETUP
        # ---------------
        db = sqlite3.connect(global_db_name)  # Connect to the project database
        db_cursor = db.cursor()

        # Prep to find the searches
        search_list = "'"
        # For singular it is done inside the query string itself
        search_list += "' or search_title = '".join(self.searchJobTitle)
        search_list += "'"

        salaryEstNumbersList = [0, 0, 0, 0, 0]

        # Query
        query = '''
              SELECT salary_est
              from listing
              where hash_val
              in
              (
              select hash_val
              from junction
              where search_hash
              in
              (
              select search_hash
              from search
              where search_title = {}));
              '''.format(search_list)

        for row in db_cursor.execute(query):

            for i in range(len(row)):
                if (row[i] == '$14,000'):
                    temp = salaryEstNumbersList[0]
                    temp = temp + 1
                    salaryEstNumbersList[0] = temp
                elif (row[i] == '$30,000'):
                    temp = salaryEstNumbersList[1]
                    temp = temp + 1
                    salaryEstNumbersList[1] = temp
                elif (row[i] == '$50,000'):
                    temp = salaryEstNumbersList[2]
                    temp = temp + 1
                    salaryEstNumbersList[2] = temp
                elif (row[i] == '$70,000'):
                    temp = salaryEstNumbersList[2]
                    temp = temp + 1
                    salaryEstNumbersList[2] = temp
                elif (row[i] == '$90,000'):
                    temp = salaryEstNumbersList[2]
                    temp = temp + 1
                    salaryEstNumbersList[2] = temp
                #print(row[i])

        #print(salaryEstNumbersList)

        objects = ('$14,000','$30,000','$50,000','$70,000','$90,000')
        y_pos = np.arange(len(objects))

        plt.bar(y_pos, salaryEstNumbersList, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.xlabel('Salary Levels')
        plt.ylabel('Number of Positions')
        plt.title('{0} Salary Estimate Graph'.format(search_list))

        plt.show()













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





