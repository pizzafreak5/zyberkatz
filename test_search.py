import search 
import sqlite3
import db

search_options = {
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

'''    
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

for row in db_cursor.execute('SELECT * FROM temporary'):
    print ('ENTRY:\n**********************************************************')
    for i in range(len(row)):
        print (column_names[i] + ':' + row[i])
    print('**********************************************************\n')


'''