# zyberkatz
**Program description:**

This GUI application searches Indeed.com for a job search specified by the user. The results are stored in a SQLite database. You can view the results from the search as well as search for analytics based on the job title.

**Setup directions:**

 - Git clone the repo into a local folder on your machine. 
 - Open the project in Pycharm or your preferred method of running a python program
 - Verify you have Python version 3.6.0 on your machine.
 - Verify the following packages are in your interpreter for the program: beautifulsoup4, bs4, matplotlib, numpy, pandas, sqlite3, datetime, hashlib, json, tkinter, scraper.


**Usage:**

- Execute GUI.py to begin the application. 
- Fill out the fields for the job type and location you want to get data on. Give in a name for the search and press the 'Search Indeed.com' button. The search itself will take a few minutes...
- Any notifications will be displayed on the lower grey bar on the GUI.
- Once the search says it's complete, you can go to the results tab to view analytics.
- You can select one or multiple searches to then select one of the buttons below. 
- With the 'Create a new Search...' button, you can text search through the selected searches. 
- The 'Analytics' search opens up a new Analytics GUI. You can select to view bar or pie graphs based on multiple categories. 
- The 'Delete Selected Entries' simply deletes the searches you have selected. 
