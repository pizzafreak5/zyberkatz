import scraper
import sqlite3
import json

#Usages Examples

#'''generate url
file = open('url.json', 'r')        #open the json file
url_dict = json.load(file)          #load it in as a dictionary
url = scraper.generate_url(url_dict)#use the dictionary to assemble a url
print (url)                         #show the url
#'''

###################################
#######DATABASE AND SCRAPING#######
###################################
#Preparing the sqlite3 database for scraper.py
listings = sqlite3.connect(':memory:')          #Create a database in ram
                                                #Change :memory: to a different value to not be in ram
db_cursor = listings.cursor()                   #Create a cursor that will be passed into scraper.py
#Create the table that will be used by scraper.py
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
listings.commit()

#dict for settings that is passed to a scraper object                     
settings = {
    'website_url' : 'http://www.indeed.com/jobs?q=Computer+Science&l=Denver%2C+CO',
    'div_class_links':'pagination',     
    'div_class_listings':['  row  result', 'row  result',  'lastRow  row  result', 'row result', ' row result', ' lastRow row result', 'lastRow row result'],
    'job_type':'',
    'salary_est':'',
    'company_name_tag':'span',
    'company_name_attrs':{'class':'company'},
    'time_posted_tag':'span',
    'time_posted_attrs':{'class':'date'},
    'job_loc_tag':'span',
    'job_loc_attrs':{'class':'location'},
    'job_desc_tag':'span',
    'job_desc_attrs':{'class':'summary'},
    'job_title_tag':'a'
    }
    #SETTINGS EXPLAINED
    #website_url: the website url you want to query (indeed.com)
    #div_class_links: the div class name for the next page of results, used to generate additional urls for more results
    #div_class_listings: python list of names of div class names for all results
    #company_name_tag: the html tag used to display the company name
    #company_name_attrs: the attributes used to identify the specific tag inside the div
    #time_posted_tag: the html tag used to display the time posted
    #time_posted_attrs: the attributes used to identify the specific tag inside the div
    #job_loc_tag: the html tag used to display the job location
    #job_loc_attrs: the attributes used to identify the specific tag inside the div
    #job_desc_tag: the html tag used to display the job description
    #job_desc_attrs: the attributes used to identify the specific tag inside the div
    #job_title_tag: the html tag used to display the job title, right now it's a link to the job posting
    #OPTIONAL SETTINGS
    #https: the value passed in here is used to append before www. of a url to give the right protocol for requests, default is http://
    #limit: the amount of pages that will be scraped, default is 1
    #headers: the headers used for requests
    #experience: the value used when inserting into the database for experience
    #salary_est: the value used when inserting into the database for salary estimates
    #job_type: the value used when inserting into the database for the job type
                           
#'''Create a new scraper object and scrape
#It needs the settings dictionary, the database cursor, and the table name you want to use
scraper1 = scraper.scraper(settings, db_cursor, "listings") 
scraper1.scrape(scraper1.url)                   #Start it with the initial url provided
#'''

#Save the Entries
listings.commit()

#Names to the respective columns
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

#Show the entries in the database
for row in db_cursor.execute('SELECT * FROM listings'):
    print ('ENTRY:\n**********************************************************')
    for i in range(len(row)):
        print (column_names[i] + ':' + row[i])
    print('**********************************************************\n')


















