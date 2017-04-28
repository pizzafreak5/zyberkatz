# zyberkatz KATTZ webscraper
**Program description:**

This GUI application searches Indeed.com for a job search specified by the user. The results are stored in a SQLite database. You can view the results from the search as well as search for analytics based on the job title.

**Setup directions:**

 - Git clone the repo into a local folder on your machine. 
 - Verify you have Python version 3.6.0 on your machine. On command line run, `python -V`
 - Open up a terminal in the directory of the cloned github repo and execute "python setup.py install", this will install all the packages listed in install_requires in the file setup.py which should then install all the required packages to use this project.
 
 - Verify the following packages are in your interpreter for the program: 
 
 1. beautifulsoup4
 2. matplotlib
 3. numpy
 4. pandas
 5. datetime
 6. lxml
 7. requests

 
 
 - If packages are not installed...
 
 from command line download pip by executing
 
 
 `curl https://bootstrap.pypa.io/ez_setup.py | python`
 
 if that doesn't work follow [this link](https://packaging.python.org/installing/#use-pip-for-installing)
 
 then
 
 
 `curl https://bootstrap.pypa.io/get-pip.py | python`
 
 then execute
 
 `pip install <package name>`
 
 If something still doesn't work in the program, make sure you have the following Python packages installed on your machine
 
 1. sqlite3
 2. hashlib  
 3. json 
 4. tkinter
 5. re
 6. url.libparse 
 7. timedelta
 8. webbrowser 
 9. csv
 10. threading
 
**GUI Layout**

 - main GUI contains: 2 tabs search and results, 2 menu options Zyber Katz and Menu.
 - Search tab contains: 2 fields (job titles and location) with 1 correlating field (search name) and 1 initiation search button. Status bar at bottom of view.
 - Results tab contains: list box containing previous searches, 3 buttons (Create a new Search From the above, analytics, and Delete Selected Entries).
 - 'Create new search from the above' GUI contains: custom text search on the selected categories (noted at top of GUI), also a save button to store text searches within the listbox of the Results view.
 - 'Analytics' GUI contains: results chart (displays a table of entries from the search(es) selected). The salary estimates, job experience, and job type can all be displayed in either pie charts or bar graphs.
 - 'Delecte selected entries' button: deletes whatever entries you have selected.
 - Zyber Katz menu option: has an about section that displays a disclaimer and an about section on the program. 
 - Menu menu option: Export jobs, reset search fields, and exit. Export jobs, 

**Usage:**

- Execute GUI.py to begin the application. 
- Fill out the search fields for the job type, location, and title for this partical search. Press the 'Search Indeed.com' button to comence the query. The search itself will take a few minutes...
- The bottom status bar will notify once query has completed.
- Once the search says it's complete, you can go to the results tab to view analytics and perform custom text searches.
- You can select one or multiple searches to then select one of the buttons below.
- Click on the Analytics button to view a results table, pie charts, and bar graph for selected previous searches.
- There are saving options for pie charts, bar graphs and query databases.
