import search 
import sqlite3
import db

search_options = {'search_title':'something',
                       'search_value':'COMPUTER SCIENC',
                       'job_location':'DENVER, CO',
                       'job_salary_est':'',
                       'limit':'',
                       'job_type':'',
                       'job_experience':'',
                       'website_url':'',
                       'global_listings_table':'listing',
                       'global_search_table':'search',
                       'global_search_junction': 'search_junction',
                       'global_db_name':'zyber.db'}


search_obj = search.Search(search_options)
search_obj.search()

global_db_name = 'zyber.db'
#---------------
#DB SETUP
#---------------
db = sqlite3.connect(global_db_name) #Connect to the project database
db_cursor = db.cursor()

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

for row in db_cursor.execute('SELECT * FROM search'):
    print ('ENTRY:\n**********************************************************')
    for i in range(len(row)):
        print (row[i])
    print('**********************************************************\n')


