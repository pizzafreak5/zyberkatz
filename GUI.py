import tkinter as tk
from tkinter import ttk, filedialog, StringVar, TOP, Label, BOTTOM, SUNKEN, N, W, X,S,E, Canvas, PhotoImage, YES, BOTH
import tkinter.simpledialog
import tkinter.messagebox
import json
import search_logic
import sqlite3
import analytics_gui
import threading
import csv


aboutTxt = """
Katz Attack Triple Threat Z'craper: (KATTZ)
Licensed 2017, March 25th.

Release version # 1.0.4

This web scraper was designed to scrape and search Indeed.com
for a specified job and/or location, then storing the information
in a SQL database. It will be possible to look up analytics for the job
searches as well as comparative analytics on many of the job searches. 

Powered by open-source software
"""

disclaimer = """
Disclaimer

This tool was manufactured for a university class project. Much testing
has been performed, however unforeseen scenarios may impose undesirable
output and/or operation. There is no warranty to the output and/or operation
provided by this tool. This tool should be considered as a learning tool
and not be applied for professional applications.

Thank you,
Justin Hockenberry, Gediminas Jakstonis,
Garrett Schwartz, & Tegan Straley\n"""



root = tk.Tk()

#Variables
db_name = 'zyber.db'


search_button_font = ("arial", 20)

class GUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(root)
        root.resizable(0,0)
        root.iconbitmap('sideprofileCat.ico')
        root.wm_title("KATTZscraper")

        self.isRunning = False  # Multi-threading flag

        self.selected = []
        self.field_selected = []
        
        #Load previous information
        self.load_settings()
        
        #Setup the GUI
        self.error_search = ''      #Error string for Search Tab
        
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


        # ****** Bottom Status Bar *******
        self.message = "Awaiting your command!"
        self.statusText = StringVar()
        self.statusText.set(self.message)
        self.status = Label(root, textvariable=self.statusText, bd=1,
                            background='grey').grid(row=4, column=0, columnspan=2, sticky=W + E)

        
    def menubar(self):

        menubar = tk.Menu(root)

        # Zyber Katz
        zmenu = tk.Menu(menubar, tearoff=0)
        zmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Zyber Katz", menu=zmenu)

        # Menu
        menu = tk.Menu(menubar, tearoff=0)
        #menu.add_command(label="Import", command=self.import_info)
        menu.add_command(label="Export Jobs", command=self.export_info)
        menu.add_command(label="Reset Search Fields", command=self.reset)
        menu.add_separator()
        menu.add_command(label="Exit", command=root.destroy)
        menubar.add_cascade(label="Menu", menu=menu)

        #Edit
        #edit_menu = tk.Menu(menubar, tearoff=0)
		
        root.config(menu=menubar)
    
    def create_search(self, root):
        global search_button_font

        # ****** Default Input Values *******
        self.default_job_title = StringVar(value="ex: Cyber Security")
        self.default_location = StringVar(value="ex: Washington, DC")
        self.default_search_name = StringVar(value="ex: CyberSec DC")


        #job title
        tk.Label(root, background='light grey',text="Job Title:").grid(row=0, column=0, sticky = W+E, padx=15, pady=10)
        #Input
        self.job_title = tk.Entry(root, highlightbackground='light grey', textvariable=self.default_job_title)
        self.job_title.grid(row=0, column=1,padx=10, pady=5)
        
        #Location
        tk.Label(root, background='light grey',text="Location:").grid(row=1, column=0, sticky = W+E, padx=15, pady=10,)

        #Input
        self.location = tk.Entry(root, highlightbackground='light grey', textvariable=self.default_location)
        self.location.grid(row=1, column =1, padx=10, pady=5)
        
        #Search title
        tk.Label(root, background='light grey', text="Search Name:").grid(row=2, column=0,sticky = W+E, padx=15, pady=10)
        #Input
        self.search_name = tk.Entry(root, highlightbackground='light grey', textvariable=self.default_search_name)
        self.search_name.grid(row=2, column =1, padx=10, pady=5,)
        
        #search button
        self.search_button = tk.Button(root,highlightbackground='light grey', text="Search Indeed.com",
                                       font= search_button_font, command=self.play).grid(row=3, column=0, columnspan=2, sticky = W+E,  pady=30, padx=20)
        
        #Error output
        #self.error_search_output = tk.Label(root, text=self.error_search).grid(row=4, column=0)

    def updateStatus(self, textVar):
        self.statusText.set(textVar)

    def create_search_selection(self, root):
        #globals used        
        self.search_list = tk.Listbox(root, selectmode=tk.EXTENDED, 
                                height=5,width=32, exportselection=False)
                
        for search in self.searches:
            self.search_list.insert(tk.END, search)
            
        for search in self.custom_searches:
            self.search_list.insert(tk.END, search)
        
        #Text
        tk.Label(root, background='light grey',text="Select a Single Search or Multiple Searches").grid(row =4, column=0, pady = 5, padx = 35)
        
        #Selection    
        self.search_list.grid(row=5, column=0, sticky= W+E, pady = 8, padx = 35)
        self.search_list.bind("<<ListboxSelect>>", self.update_search_selection)
        
        #Search The Searches
        self.search_selected_button = tk.Button(root, highlightbackground='grey',text="Create a new Search from the above",
                            command=self.search_selection).grid(row=6, column=0, sticky=tk.W + tk.E, pady = 2, padx = 35)

        #Text for analytics
        self.analytics_button = tk.Button(root, highlightbackground='grey',text="Analytics",
                            command=self.analytics).grid(row=7, column=0, sticky=tk.W + tk.E, pady = 2, padx = 35)
        
        #Text for delete search
        self.search_delete_button = tk.Button(root, highlightbackground='grey',text="Delete Selected Entries",
                                              command=self.delete_selected_searches).grid(row=8, column=0, sticky= tk.W + tk.E, pady = 2, padx = 35)
        
    def update_search_selection(self, event):
        widget = event.widget                   #Get the widget for the event
        self.selection = widget.curselection()       #Get the selection from the widget
            #selection is a tuple of choices
        
        self.selected = []
        for term in self.selection:
            self.selected.append(widget.get(term))   #Create a list of values selected

    def delete_selected_searches(self):
        from_search = []
        from_custom_search = {}
        
        for term in self.selected:
            if term in self.searches:
                from_search.append(term)
            elif term in self.custom_searches:
                from_custom_search[term] = self.custom_searches[term]

        db = sqlite3.connect(db_name)
        db_cursor = db.cursor()

        for search in from_search:
            sql_drop = '''
            DELETE FROM search
            WHERE search_title = '{}'
            '''
            self.searches.remove(search)
            
            query = sql_drop.format(search)
            db_cursor.execute(query)
            db.commit()
            
            
        for search in from_custom_search:
            self.custom_searches.pop(search, None)
        
        self.search_list.delete(0, tk.END)
        for search in self.searches:
            self.search_list.insert(tk.END, search)
            
        for search in self.custom_searches:
            self.search_list.insert(tk.END, search)
            
        self.update_idletasks()     #Update the gui
        self.update_settings()      #update the settings
    
    def import_info(self):
        print("imports")
        
    def export_info(self):
        filename = filedialog.asksaveasfilename(initialdir = '/', title='Save Export as',
                                            filetypes= (("Comma Separated Values (*.csv)", "*.csv"),))
        if filename is None:
            return
        else:
            db = sqlite3.connect(db_name)
            db_cursor = db.cursor()
            
            query = "SELECT * FROM listing"
            if self.selected:
                query = self.create_search_query(self.searches, self.custom_searches,
                                                 self.selected, [], "")
                
            print ("QUERY:",query)           
            
            row_count = 0
            with open(filename + ".csv", 'w', newline='', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_ALL)
                for row in db_cursor.execute(query):
                    row_count +=1
                    list_row = []
                    for value in row:
                        list_row.append(value)
                    writer.writerow(list_row)
            
            
            finish = "Finished writing to file " + filename + ".csv\n" + "Exported " + str(row_count) + " jobs"
            tkinter.messagebox.showinfo("Finished Exporting", finish)
        
    def analytics(self):
        if self.selected:
            query_job = self.create_search_query(self.searches, self.custom_searches, self.selected, [], "", "job_type")
            query_exp = self.create_search_query(self.searches, self.custom_searches, self.selected, [], "", "job_exp")
            query_salary = self.create_search_query(self.searches, self.custom_searches, self.selected, [], "", "salary_est")
            query_chart = self.create_search_query(self.searches, self.custom_searches, self.selected,[], "", "company, job_title, job_loc, salary_est, link")

            tmp = analytics_gui.analyticsGUI(self.selected, query_job, query_exp, query_salary, query_chart)

    def reset(self):

        # Reset and clears all fields
        self.default_job_title.set("")
        self.default_location.set("")
        self.default_search_name.set("")

        self.updateStatus("Input fields reset...")

    def about(self):
        # About option from drop down window
        # Opens new window to display About message and Disclaimer
        toplevel = tk.Toplevel()
        toplevel.iconbitmap('sideprofileCat.ico')
        label1 = tk.Label(toplevel, text=aboutTxt, background = 'light grey', height=0, width=60)
        label1.pack()
        label2 = tk.Label(toplevel, text=disclaimer, background = 'light grey', height=0, width=60)
        label2.pack()

    def play(self):

        self.updateStatus("Please wait, scanning Indeed.com...")

        try:
            # Get input
            job_title = self.job_title.get()
            location = self.location.get()
            search_title = self.search_name.get()

            if search_title == "":
                error = "Error: a search has to have a non-empty name"
                self.updateStatus("Error: a search has to have a non-empty name")
                self.error_search = error
                return

            # Verify uniqueness of search title
            if search_title in self.searches:
                error = "Error: there already exists a search with the name" + search_title
                self.updateStatus("Error: there already exists a search with the name" + search_title)
                self.error_search = error
                return
            if self.isRunning != True:  # Blocks user from initiating multiple searches
                if self.isRunning == False:
                    self.isRunning = True
                    self.scanThread = threading.Thread(target=self.new_search)
                    self.scanThread.start()
                else:
                    self.isRunning = False
                    self.updateStatus("Bad input...")
                    self.stop()
        except ValueError:
            self.isRunning = False
            self.stop()

    def new_search(self):
        try:
            # Get input
            job_title = self.job_title.get()
            location = self.location.get()
            search_title = self.search_name.get()

            # Add it to searches
            self.searches.append(search_title)

            # Do a search
            search_logic.run_search(job_title, location, search_title)

            # Update the results so that the search is visible
            self.search_list.insert(tk.END, search_title)
            self.update_settings()
            self.update_idletasks()

            if self.isRunning == True:
                self.updateStatus("Completed scanning Indeed.com...")
                try:
                    # Stops the extra thread we used to scan
                    self.isRunning = False
                    self.scanThread.join(0)
                    self.scanThread = None
                except (AttributeError, RuntimeError):  # Scan thread could be None
                    pass
        except AttributeError:
            self.updateStatus("Hostname could not be resolved. Stopping...")
        except RuntimeError:
            self.updateStatus("Couldn't connect to server")

    def stop(self):

        # If user wants to Interrupt the ongoing scan
        if self.isRunning != False:
            self.updateStatus("Operation Stopped...")

        try:
            # Stops the extra thread we used to scan
            self.isRunning = False
            self.scanThread.join(0)
            self.scanThread = None

        except (AttributeError, RuntimeError):  # Scan thread could be None
            pass

    def load_settings(self):
        self.searches = []
        self.custom_searches = {}
        try:
            with open('kattz.searches.json') as settings:
                self.searches = json.load(settings)
        except:
            print ("Failed to find file kattz.searches.json\n")
            
        try:
            with open('kattz.custom_searches.json') as custom_search:
                self.custom_searches = json.load(custom_search)
        except:
            print("Failed to find file kattz.custom_searches.json\n")
            
    def update_settings(self):
        with open('kattz.searches.json', 'w') as settings:
            settings.seek(0)
            write_string = json.dumps(self.searches)
            settings.write(write_string)
            settings.truncate()
            settings.close()
            
        with open('kattz.custom_searches.json', 'w') as settings:
            settings.seek(0)
            write_string = json.dumps(self.custom_searches)
            settings.write(write_string)
            settings.truncate()
            settings.close()
            
    def search_selection(self):
        text_search = tk.Toplevel()
        text_search.wm_title("Text Search")
        text_search.iconbitmap('sideprofileCat.ico')
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
        self.search_text_output.config(state=tk.NORMAL)                 #Allow writing
        self.search_text_output.delete('1.0', tk.END)                   #clear the output
        self.search_text_output.config(state=tk.DISABLED)               #No writing
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
        
        if search_term != ""and not self.field_selected:
            self.output_to_search_text("No field to search for " + search_term)
            return
        
        #Create the database connection
        db = sqlite3.connect(db_name)
        db_cursor = db.cursor()
        
        query = self.create_search_query(self.searches, self.custom_searches, self.selected, self.field_selection, search_term)
                
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
        return query
    
    def search_save(self):
        query = self.search_text()
        print (query)
        
        search_name = tkinter.simpledialog.askstring("Save search as", "Please enter a search name for this search")
        
        #Error checking
        if search_name in self.searches or search_name == '' or search_name in self.custom_searches:
            #Error conflicts with an existing search name
            error = "'" + search_name + "'" + " is either already used as a search name or is an invalid search name"
            tkinter.messagebox.showerror("Invalid search name", error)
            return                      #Couldnt save
            
        #Add to the selection listbox
        self.search_list.insert(tk.END, search_name)
        self.update_idletasks()
        #Add to saved_searches
        self.custom_searches[search_name] = query
        #Populate saved information
        self.update_settings()
    
    def prepare_search_text_statement(self, field_selection, search_term):
        fields = ("company", "time_posted", "job_title", "job_desc", "job_loc", 
                      "job_exp", "salary_est", "job_type", "link", "job_text")
        selected_fields = []            #have to reconstruct with database names
        
        for i in field_selection:       #From user selected names
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
        
        return field_string

    def output_to_search_text(self, message, clear = False):
        self.search_text_output.config(state=tk.NORMAL)     #Allow text writing to box
        if (clear == True):                                 #Clear box?
            self.search_text_output.delete('1.0', tk.END)   #Clear box
        self.search_text_output.insert(tk.END, message)     #Write from bottom down
        self.search_text_output.config(state=tk.DISABLED)   #Prevent more writing
        
    def create_search_query(self, searches, custom_searches, selected_searches, selected_fields, search_text, SELECT = '*'):
        #Split selected into searches and custom searches
        
        search_text = search_text.lower()
        from_search = []
        from_custom_search = {}
        
        for term in selected_searches:
            if term in searches:
                from_search.append(term)
            elif term in custom_searches:
                from_custom_search[term] = custom_searches[term]
        
        query = ""
        
        if from_custom_search:
            for key in from_custom_search:
                partial_query = from_custom_search[key]
                
                #Get rid of semicolon at the end
                if partial_query.endswith(";"):
                    partial_query = partial_query[:-1]
                
                if query == "":             #1st value from_custom_search
                    query += partial_query
                else:                       #2nd+ value from_custom_search
                    query += " UNION " + partial_query
            
            if from_search: #there is also a normal search
                sub_query = self.create_search_query_from_searches(from_search, SELECT)
                query += " UNION " + sub_query 
                        
            qstring = '''
            SELECT {} FROM listing
            WHERE hash_val IN ({})
            '''
            query = query.replace("SELECT *", "SELECT hash_val")
            query = qstring.format(SELECT, query)
            
            if search_text != "":
                and_query = " AND (" + self.prepare_search_text_statement(selected_fields, search_text) + ")"
                query += and_query

            query += ";"
            return query
            
        #no custom search, normal search only
        elif from_search: 
            query = self.create_search_query_from_searches(from_search , SELECT)
            if search_text != "":   #there is a text search
                query += " AND (" + self.prepare_search_text_statement(selected_fields, search_text) + ");"
            return query
        
    def create_search_query_from_searches(self, searches, SELECT = '*'):
        
        #Prep to find the searches
        search_list = "'"
        #For singular it is done inside the query string itself
        search_list += "' or search_title = '".join(searches) 
        search_list += "'"
        
        #Query to grab all searches based on the name(s) in searches
        query = '''
        SELECT {}
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
        '''.format(SELECT, search_list)
        
        return query
        
    def sql_test(self):
        db = sqlite3.connect(db_name)
        db_cursor = db.cursor()
        
        self.load_settings()
        self.custom_searches = {}
        

        search_term = "coffee"
        search_term = ""
        #   TEST 1
        #   Check to see if all the normal searches work like they should and then query all of them
        for search in self.searches:
            row_count =  0
            selected = []
            selected.append(search)
            query = self.create_search_query(self.searches, self.custom_searches, selected, "", search_term)
                                            #all searches, all custom searches, selected searches, selected fields, search term
            for row in db_cursor.execute(query):
                row_count += 1
            
            print ("search:", search, "\trows:", row_count)
        query = self.create_search_query(self.searches, self.custom_searches, self.searches, "", search_term)
        row_count = 0
        for row in db_cursor.execute(query):
            row_count +=1
        print ("search:", self.searches, "\trows:", row_count)  #Expect 84
        
        #   TEST 2
        #   Create a custom search from normal searches
        search_name = "test2"
        search_term = "coffee"
        selected_fields = (3,)
        print ("search:", search_name, "\t\tterm:", search_term, end="\t")
        query = self.create_search_query(self.searches, self.custom_searches, self.searches, selected_fields, search_term)
        self.custom_searches[search_name] = query
        row_count = 0
        for row in db_cursor.execute(query):
            row_count += 1
        print ("rows:", row_count) #expect 25
        
        #   TEST 3
        #   create a custom search from a custom search
        search_name = "test3"
        search_term = "shop"
        selected_fields = (3,)
        print ("search:", search_name, "\t\tterm:", search_term, end="\t")
        query = self.create_search_query(self.searches, self.custom_searches, self.custom_searches, selected_fields, search_term)
        self.custom_searches[search_name] = query
        row_count = 0
        for row in db_cursor.execute(query):
            row_count +=1
        print ("rows:", row_count) #Expect 6
        
        #   TEST 4
        #   create a custom search from 2 custom searches
        search_name = "test4"
        search_term = "resume"
        selected_fields = (3,)
        print ("search:", search_name, "\t\tterm:", search_term, end="\t")
        if (len(self.custom_searches) != 2):
            print ("EXPECTED 2 CUSTOM SEARCHES TO EXIST")
        query = self.create_search_query(self.searches, self.custom_searches, self.custom_searches, selected_fields, search_term)
        self.custom_searches[search_name] = query
        row_count = 0
        for row in db_cursor.execute(query):
            row_count +=1
        print ("rows:", row_count)
        
        #   TEST 5
        #   Create a custom search from 2 custom searches and 2 normal searches
        search_name = "test5"
        search_term = "focus"
        selected_fields = (3,)
        print ("search:", search_name, "\t\tterm:", search_term, end="\t")
        selected = ['test4', 'test3']
        for i in range(len(self.searches)):
            selected.append(self.searches[i])
            if i == 1:
                break
        query = self.create_search_query(self.searches, self.custom_searches, selected, selected_fields, search_term)
        self.custom_searches[search_name] = query
        row_count = 0
        for row in db_cursor.execute(query):
            row_count +=1
        print ("rows:", row_count)
        
        with open('test.json', 'w') as settings:
            settings.seek(0)
            write_string = json.dumps(self.custom_searches)
            settings.write(write_string)
            settings.truncate()
            settings.close()
        
        #Remove all custom searches done for the tests
        self.load_settings()
        
        
app = GUI()
#app.sql_test()
app.mainloop()
