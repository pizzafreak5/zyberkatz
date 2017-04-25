import tkinter as tk
from tkinter import ttk, StringVar, TOP, Label, BOTTOM, SUNKEN, N, W, X,S,E, Canvas, PhotoImage, YES, BOTH
import tkinter.simpledialog
import tkinter.messagebox
import json
import search_logic
import sqlite3
import analytics_gui
import threading

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
db_name = 'zyber.db'


search_button_font = ("arial", 12)

class GUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(root)
        root.resizable(0,0)
        root.iconbitmap('sideprofileCat.ico')
        root.wm_title("KATTZraper")

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
        zmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Zyber Katz", menu=zmenu)
		
        root.config(menu=menubar)
    
    def create_search(self, root):
        global search_button_font

        #job title
        tk.Label(root, background='light grey',text="Job Title:").grid(row=0, column=0, sticky = W+E)
        #Input
        self.job_title = tk.Entry(root)
        self.job_title.grid(row=0, column=1)
        
        #Location
        tk.Label(root, background='light grey',text="Location:").grid(row=1, column=0, sticky = W+E)
        #Input
        self.location = tk.Entry(root)
        self.location.grid(row=1, column =1)
        
        #Search title
        tk.Label(root, background='light grey', text="Search Name:").grid(row=2, column=0)
        #Input
        self.search_name = tk.Entry(root)
        self.search_name.grid(row=2, column =1)
        
        #search button
        self.search_button = tk.Button(root,highlightbackground='light grey', text="Search Indeed.com", font= search_button_font, command=self.play).grid(row=3, column=0, columnspan=2, sticky = W+E)
        
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
        tk.Label(root, background='light grey',text="Select a Single Search or Multiple Searches").grid(row =4, column=0)
        
        #Selection    
        self.search_list.grid(row=5, column=0)
        self.search_list.bind("<<ListboxSelect>>", self.update_search_selection)
        
        #Search The Searches
        self.search_selected_button = tk.Button(root, highlightbackground='grey',text="Create a new Search from the above",
                            command=self.search_selection).grid(row=6, column=0, sticky=tk.W + tk.E)        

        #Text for analytics
        self.analytics_button = tk.Button(root, highlightbackground='grey',text="Analytics",
                            command=self.analytics).grid(row=7, column=0, sticky=tk.W + tk.E)
        
        #Text for delete search
        self.search_delete_button = tk.Button(root, highlightbackground='grey',text="Delete Selected Entries",
                                              command=self.delete_selected_searches).grid(row=8, column=0, sticky= tk.W + tk.E)
        
    def update_search_selection(self, event):
        widget = event.widget                   #Get the widget for the event
        self.selection = widget.curselection()       #Get the selection from the widget
            #selection is a tuple of choices
        
        self.selected = []
        for term in self.selection:
            self.selected.append(widget.get(term))   #Create a list of values selected

    def delete_selected_searches(self):
        print("delete selected searches")
    
    def import_info(self):
        print("imports")
        
    def export_info(self):
        print("export")
        
    def analytics(self):
        searchJobTitle = self.selected
        tmp = analytics_gui.analyticsGUI(searchJobTitle)

    def about(self):
        # About option from drop down window
        # Opens new window to display About message and Disclaimer
        toplevel = tk.Toplevel()
        toplevel.iconbitmap('sideprofileCat.ico')
        label1 = tk.Label(toplevel, text=aboutTxt, height=0, width=60)
        label1.pack()
        label2 = tk.Label(toplevel, text=disclaimer, height=0, width=60)
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
        print (query)
                
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
        if from_custom_search:  #There is a saved search selected
            if len(from_custom_search) > 1:
                #Multiple custom searches selected
                query += "("
                count = 0
                for key in from_custom_search:
                    partial_query = from_custom_search[key]
                    #the query that is appended has a semicolon at the end
                    if partial_query.endswith(";"):
                        partial_query = partial_query[:-1] #remove the ;
                    
                    #Last value
                    if (count == len(from_custom_search) - 1):
                        query += partial_query
                        
                    else:
                        query += " OR " + partial_query
                query += ")"
            else:
                #Single custom search selected
                for key in from_custom_search:
                    partial_query = from_custom_search[key]
                    #the query that is appended has a semicolon at the end
                    if partial_query.endswith(";"):
                        partial_query = partial_query[:-1] #remove the ;
                    query += partial_query
                                    
        
        if from_search:             #There is something selected that is from an original search
            #query selects all the real searches    
            if query == "":
                query = self.create_search_query_from_searches(from_search, SELECT)
            else:
                query += " OR " + self.create_search_query_from_searches(from_search, SELECT)
                
            if from_custom_search:
                query = "(" + query + ")"
            
        if search_text != "":
            query += "AND (" + self.prepare_search_text_statement(selected_fields, 
                                            search_text) + ")"
        if query.endswith(";") == False:
            query += ";"
        
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
	 
app = GUI()
app.mainloop()