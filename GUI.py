import tkinter as tk
from tkinter import ttk
import json
import search_logic
import sqlite3


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



root = tk.Tk()

#Variables
searches = []                           #List of searches
db_name = 'zyber.db'
scalar_n = 2

#Variables for search
search_starting_row = 0
search_starting_column = 0
search_button_font = ("arial", 12)

#Variables for selection
selection_height = 5
selection_width = 30
selection_row = 4
selection_column = 4

class GUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(root)
        root.resizable(0,0)
        
        self.selected = []
        self.field_selected = []
        
        #Load previous information
        self.load_settings()
        
        #Setup the GUI
        self.error_search = ''
        
        self.menubar()

        #Create a notebook and two frames search and resuults
        self.notebook = ttk.Notebook(root)
        self.search = ttk.Frame(self.notebook)
        self.results = ttk.Frame(self.notebook)
        
        self.notebook.add(self.search, text='Search')
        self.notebook.add(self.results, text='Results')
        self.notebook.grid(row = 0, column = 0)
        
        #Create the Elements for search
        self.create_search(self.search)
        
        #Create the elements for results
        self.create_search_selection(self.results)
        
    def menubar(self):

        menubar = tk.Menu(root)

        # Menu
        menu = tk.Menu(menubar, tearoff=0)
        #menu.add_command(label="Import", command=self.import_info)
        menu.add_command(label="Export", command=self.export_info)
        menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Menu", menu=menu)

        #Edit
        #edit_menu = tk.Menu(menubar, tearoff=0)
        
        #Zyber Katz
        zmenu = tk.Menu(menubar, tearoff=0)
        #zmenu.add_command(label="About", command=about)
        menubar.add_cascade(label="Zyber Katz", menu=zmenu)
		
		
        root.config(menu=menubar)
    
    def create_search(self, root):
        global search_starting_row, search_starting_column, search_button_font
        #job title
        tk.Label(root, text="Job Title").grid(row=search_starting_row, column = search_starting_column)
        #Input
        self.job_title = tk.Entry(root)
        self.job_title.grid(row=search_starting_row, column = search_starting_column + 1)
        
        #Location
        tk.Label(root, text="Location").grid(row=search_starting_row+1, column = search_starting_column)
        #Input
        self.location = tk.Entry(root)
        self.location.grid(row=search_starting_row+1, column = search_starting_column+1)
        
        #Search title
        tk.Label(root, text="Search Name").grid(row=search_starting_row+2, column = search_starting_column)
        #Input
        self.search_name = tk.Entry(root)
        self.search_name.grid(row=search_starting_row+2, column = search_starting_column+1)
        
        #search button
        self.search_button = tk.Button(root, text="Search Indeed.com", font= search_button_font, command=self.new_search).grid(row=search_starting_row+3, column=search_starting_column, columnspan=2)        
        
        #Error output
        self.error_search_output = tk.Label(root, text=self.error_search).grid(row = search_starting_row+4, column = search_starting_column)
    
    def create_search_selection(self, root):
        #globals used
        global searches, selection_height, selection_width, selection_row, selection_column
        
        self.search_list = tk.Listbox(root, selectmode=tk.EXTENDED, 
                                height = selection_height, width = selection_width, exportselection=False)
                
        for search in searches:
            self.search_list.insert(tk.END, search)
        
        #Text
        tk.Label(root, text="Select a search or multiple searches").grid(row = selection_row, column = selection_column)
        
        #Selection    
        self.search_list.grid(row = selection_row +1, column = selection_column)
        self.search_list.bind("<<ListboxSelect>>", self.update_search_selection)
        
        #Search The Searches
        self.search_selected_button = tk.Button(root, text="Create a new Search from the above", command=self.search_selection).grid(row=selection_row+2, column=selection_column, columnspan=2)        

        #Text for analytics
        self.analytics_button = tk.Button(root, text="Analytics", command=self.analytics).grid(row=selection_row+3, column=selection_column, columnspan=2)
        
    def update_search_selection(self, event):
        widget = event.widget                   #Get the widget for the event
        self.selection = widget.curselection()       #Get the selection from the widget
            #selection is a tuple of choices
        
        self.selected = []
        for term in self.selection:
            self.selected.append(widget.get(term))   #Create a list of values selected

    def import_info(self):
        print("imports")
        
    def export_info(self):
        print("export")
        
    def analytics(self):
        print("analytics")
        
    def new_search(self):
        global searches
        #Get input
        job_title = self.job_title.get()
        location = self.location.get()
        search_title = self.search_name.get()
        
        if search_title == "":
            error = "Error: a search has to have a non-empty name"
            self.error_search = error
            return
        
        #Verify uniqueness of search title
        if search_title in searches:
            error = "Error: there already exists a search with the name" + search_title
            self.error_search = error
            return
        
        #Add it to searches
        searches.append(search_title)
        
        #Do a search
        search_logic.run_search(job_title, location, search_title)
            
        #Update the results so that the search is visible
        self.search_list.insert(tk.END, search_title)
        self.update_settings()
        self.update_idletasks()
    
    def load_settings(self):
        global searches
        try:
            with open('kattz.settings.json') as settings:
                searches = json.load(settings)
        except:
            print ("Failed to find file kattz.settings.json")
            
    def update_settings(self):
        global searches
        with open('kattz.settings.json', 'w') as settings:
            settings.seek(0)
            write_string = json.dumps(searches)
            settings.write(write_string)
            settings.truncate()
            settings.close()
            
    def search_selection(self):
        text_search = tk.Toplevel()
        text_search.wm_title("Text Search")
        text_search.resizable(0,0)
        
        #TextSearch
        tk.Label(text_search, text="Text Search - Select the wanted columns to search and the text value").grid(row=0, column=0, columnspan=5)
        
        #Input

        #search fields input
        fields = ("Company Name", "Time Posted", "Job Title", "Job Description",
                  "Job Location", "Job Experience", "Salary Estimate", "Job Type", 
                  "URL Link","Job Posting Text")
        
        self.field_selection = tk.Listbox(text_search, selectmode=tk.EXTENDED,
                                          height=len(fields), width=100, exportselection=False)
        for field in fields:
            self.field_selection.insert(tk.END, field)
        self.field_selection.grid(row=1, column=0, columnspan =5)
        self.field_selection.bind("<<ListboxSelect>>",self.update_field_selection)
        
        #search value input
        self.input_text_search = tk.Entry(text_search, width=75)
        self.input_text_search.grid(row=2, column=0, columnspan=3)

        
        #Button Search
        self.search_text_button = tk.Button(text_search, text="Search", 
                                            command=self.search_text).grid(row=2, column=3, columnspan=1, sticky=tk.W + tk.E)    
        
        #Button Save
        self.search_save_button = tk.Button(text_search, text="Save",
                                            command=self.search_save).grid(row=2, column=4, columnspan=1, sticky=tk.W + tk.E)
        
        #Output
        self.search_text_output = tk.Text(text_search, height=20, width=80)
        self.search_text_output.config(state=tk.NORMAL)
        self.search_text_output.delete('1.0', tk.END)                   #clear the output
        self.search_text_output.config(state=tk.DISABLED)
        self.search_text_output.grid(row=3, column=0, columnspan=5)
        
    def update_field_selection(self, event):
        widget = event.widget
        self.field_selection = widget.curselection()
        
        self.field_selected = []
        for term in self.field_selection:
            self.field_selected.append(widget.get(term))
        
    def search_text(self):        
        #There is no searches selected
        if not self.selected:
            self.output_to_search_text("No search has been selected to be used", clear = True)
            return
            
        #Grab the search text value
        search_term = self.input_text_search.get()
        search_term = search_term.lower()
        
        if search_term != ""and not self.field_selected:
            self.output_to_search_text("No field to search for " + search_term)
            return
        
        
        #Create the database connection
        db = sqlite3.connect(db_name)
        db_cursor = db.cursor()
        
        #Prep to find the searches
        search_list = "'"
        #For singular it is done inside the query string itself
        search_list += "' or search_title = '".join(self.selected) 
        search_list += "'"
        
        #Prep to search the appropriate fields
        fields = ("company", "time_posted", "job_title", "job_desc", "job_loc", 
                      "job_exp", "salary_est", "job_type", "link", "job_text")
        
        selected_fields = []            #have to reconstruct with database names
        for i in self.field_selection:  #From user seen names
            selected_fields.append(fields[i])
        
        field_string = ""
        for i in range(len(selected_fields)):
            if len(selected_fields) == 1:
                field_string += "lower({}) LIKE '%{}%'".format(selected_fields[i], search_term)
            else:
                if (len(selected_fields)-1 != i):
                    field_string += "lower({}) LIKE '%{}%' or ".format(selected_fields[i], search_term)
                else:
                    field_string += "lower({}) LIKE '%{}%'".format(selected_fields[i], search_term)
                        
        #Query
        query = '''
        SELECT *
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
        where search_title = {}))
        '''.format(search_list)
        
        if search_term != "":
            query += "AND (" + field_string + ")"
        
        query += ";"
        
        results = ""
        stop_writing = False
        result_count = 0
        for row in db_cursor.execute(query):
            result_count +=1
            if (result_count >= 100):
                if stop_writing == False:
                    results += "More results may exist, please export search to view all of them\n"
                    stop_writing = True
            else:
                results += '|'.join(map(str, row))
                results += '\n\n'
        
        results = "Total results:" + str(result_count) + "\n\n" + results
        self.output_to_search_text(str.encode(results), True)
    
    def search_save(self):
        #Identical to search_text
        #There is no searches selected
        if not self.selected:
            self.output_to_search_text("No search has been selected to be used", clear = True)
            return
            
        #Grab the search text value
        search_term = self.input_text_search.get()
        search_term = search_term.lower()
        
        if search_term != ""and not self.field_selected:
            self.output_to_search_text("No field to search for " + search_term)
            return
        
        
        #Create the database connection
        db = sqlite3.connect(db_name)
        db_cursor = db.cursor()
        
        #Prep to find the searches
        search_list = "'"
        #For singular it is done inside the query string itself
        search_list += "' or search_title = '".join(self.selected) 
        search_list += "'"
        
        #Prep to search the appropriate fields
        fields = ("company", "time_posted", "job_title", "job_desc", "job_loc", 
                      "job_exp", "salary_est", "job_type", "link", "job_text")
        
        selected_fields = []            #have to reconstruct with database names
        for i in self.field_selection:  #From user seen names
            selected_fields.append(fields[i])
        
        field_string = ""
        for i in range(len(selected_fields)):
            if len(selected_fields) == 1:
                field_string += "lower({}) LIKE '%{}%'".format(selected_fields[i], search_term)
            else:
                if (len(selected_fields)-1 != i):
                    field_string += "lower({}) LIKE '%{}%' or ".format(selected_fields[i], search_term)
                else:
                    field_string += "lower({}) LIKE '%{}%'".format(selected_fields[i], search_term)
                        
        #Query
        query = '''
        SELECT *
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
        where search_title = {}))
        '''.format(search_list)
        
        if search_term != "":
            query += "AND (" + field_string + ")"
        
        query += ";"
        #SQL to save
        
    def output_to_search_text(self, message, clear = False):
        self.search_text_output.config(state=tk.NORMAL)
        if (clear == True):
            self.search_text_output.delete('1.0', tk.END)
        self.search_text_output.insert(tk.END, message)
        self.search_text_output.config(state=tk.DISABLED)
        



	 
app = GUI()
app.mainloop()