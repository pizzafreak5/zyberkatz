
import sqlite3
import tkinter as tk
from tkinter import *
import webbrowser


# Font size for the title
LARGE_FONT = ("fixedsys", 18)
SMALL_FONT = ("arial", 7)
BUTTON_FONT = ("arial", 14)

global_db_name = 'zyber.db'
#rowNumber = 1




class ResultsChart(tk.Tk):
    def __init__(self, queryChart):
        tk.Tk.__init__(self)
        self.queryChart = queryChart
        self.grabJobTitle()


    def grabJobTitle(self):

        row_info = ['Company',
                    'Job title',
                    'Location',
                    'Salary',
                    'Web Links']
        # ---------------
        # DB SETUP
        # ---------------
        db = sqlite3.connect(global_db_name)  # Connect to the project database
        db_cursor = db.cursor()

        # # Prep to find the searches
        # search_list = "'"
        # # For singular it is done inside the query string itself
        # search_list += "' or search_title = '".join(searchJobTitle)
        # search_list += "'"
        #
        # # Query
        # query = '''
        #         SELECT company, job_title, job_loc, salary_est, link
        #         from listing
        #         where hash_val
        #         in
        #         (
        #         select hash_val
        #         from junction
        #         where search_hash
        #         in
        #         (
        #         select search_hash
        #         from search
        #         where search_title = {}));
        #         '''.format(search_list)
        rowNumber = 1
        for row in db_cursor.execute(self.queryChart):
            for i in range(len(row)):
                row_info.append(row[i])

            rowNumber += 1

        #print(rowNumber, " entries found")

        t = SimpleTable(self,row_info, rowNumber, 5)


class SimpleTable(tk.Frame):

    def callback(self, event, link):
        # print(link)
        webbrowser.open_new(link)

    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __init__(self, parent, row_info, rows=1, columns=5):

        self.canvas = tk.Canvas(parent, borderwidth=5, background="grey", height = 350, width = 1080)
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
        parent.iconbitmap('sideprofileCat.ico')
        #parent.resizable(width=False, height=False)  # Makes user unable to resize window

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

                     label = tk.Label(self, text="Job Posting", fg="blue", cursor="hand2", relief=RAISED)#,
                                                    #borderwidth = 0)#, width = 10)
                     label.bind("<Button-1>", lambda event, arg=link: self.callback(event, arg))

                else:
                    label = tk.Label(self, text="%s" % (row_info[cellCount]), relief=RAISED)#,
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

        self.vsb01 = tk.Scrollbar(parent, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.vsb01.set)

        self.vsb.pack(side="right", fill="y")
        self.vsb01.pack(side="bottom", fill="x")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0,0), window=self, anchor=N+W)
        self.bind("<Configure>", self.OnFrameConfigure)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)




if __name__ == "__main__":
    searchJobTitle =""
    app = ResultsChart(searchJobTitle)
    app.mainloop()










