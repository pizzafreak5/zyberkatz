# FILE: search.py
# Singular search request that adds entries to the database
# Written by Garrett
# Edited by Tegan


import scraper
import json
import sqlite3
import datetime
import hashlib


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Search:

    def __init__(self, search_options):

        self.search_hash = ''
        self.search_options = {'search_title':'',
                               'search_value':'',
                               'job_location':'',
                               'job_salary_est':'',
                               'limit':'',
                               'job_type':'',
                               'job_experience':'',
                               'website_url':'',
                               'global_listings_table':'listing',
                               'global_search_table':'search',
                               'global_search_junction': 'search_junction',
                               'global_db_name':'zyber.db'}

        #check for options passed in
        for key in self.search_options:
            if key in search_options:
                self.search_options[key] = search_options[key]
        

    def set_search_option(self, key, option):

        if key in self.search_options():
            self.search_options[key] = option
        else:
            err = 'search.py - set_search_option() - key {} is not a valid option key'.format(key)
        

    #How to call:  
    def search(self):

        #---------------
        #DB SETUP
        #---------------
        db = sqlite3.connect(self.search_options['global_db_name']) #Connect to the project database
        db_cursor = db.cursor()
        
        #Delete the previous table temporary
        db_cursor.execute('drop table if exists temporary')
        
        #create a new table that will be joined later to the main listings table
        db_cursor.execute('''
CREATE TABLE temporary
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

        #---------------
        #SCRAPER SETUP
        #---------------

        #Note: Add to settings a header to specify user agent as something other
        #than python
        settings = {
            'website_url' : '',
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

        url = self.__construct_url()
        settings['website_url'] = url

        for option in self.search_options:
            if option in settings:
                settings[option] = self.search_options[option]

        #---------------
        #RUN SCRAPER
        #---------------
        search_scraper = scraper.scraper(settings, db_cursor, 'temporary')

        flag = True

        while flag:
            try:
                flag = False
                search_scraper.scrape(search_scraper.url)
            except:
                flag = True
                
        
        

        #save changes to db
        db.commit()

        #---------------
        #APPEND TO SEARCH TABLE
        #---------------
        #Note: Consider changing this to UTC time.
        search_date = str(datetime.datetime.today())

        search_value = self.search_options['search_value']
        search_title = self.search_options['search_title']
        search_loc   = self.search_options['job_location']
        search_sal   = self.search_options['job_salary_est']
        search_exp   = self.search_options['job_experience']
        search_type  = self.search_options['job_type']
        
        hash_string = search_date + search_value + search_title + search_loc + search_sal + search_exp + search_type
        search_hash = hashlib.sha256((hash_string).encode('utf-8')).hexdigest()
        self.search_hash = search_hash
        
        #Create the val string to input into the DB. The order here is important
        values = (search_hash, search_title, search_date, search_value, search_loc, search_type, search_exp, search_sal)

        #Query to insert into the table search 
        q = 'INSERT INTO search (search_hash, search_title, search_date, search_value, search_loc, job_type, job_exp, job_salary_min) VALUES (?,?,?,?,?,?,?,?)'
        
        db_cursor.execute(q, values)
        db.commit()
        

        #---------------
        #APPEND TO LISTING TABLE
        #---------------

        #append the new rows onto the global listing table
        q = 'SELECT * FROM temporary WHERE hash_val NOT IN (SElECT hash_val FROM listing);'
        db_cursor.execute(q)
        temp_data = db_cursor.fetchall()
        q = 'INSERT INTO listing (hash_val, company, time_posted, job_title, job_desc, job_loc, job_exp, salary_est, job_type, link, job_text) VALUES(?,?,?,?,?,?,?,?,?,?,?);'

        for row in temp_data:
            #Create the tuple for each row
            values = tuple(row)
            
            db_cursor.execute(q, values)

        db.commit()

        #---------------
        #APPEND TO JUNCTION TABLE
        #---------------

        q = 'SELECT hash_val FROM temporary'
        db_cursor.execute(q)
        hash_values = db_cursor.fetchall()

        for row in hash_values:
            values = (row[0], search_hash)
            q = "INSERT INTO junction (hash_val, search_hash) VALUES (?,?);"
            db_cursor.execute(q, values)

        db.commit()

    #Returns the url to search
    def __construct_url(self):

        url_form_0 = 'http://www.indeed.com/jobs?q={}'
        url_form_1 = 'http://www.indeed.com/q-{}-{}-l-{}-jobs.html'#attempt to not use

        query_job_salary = '{}+{}'
        query_location = '&l={}'
        query_job_type = '&jt={}'
        query_exp_level = '&explvl={}'

        query_string = ''


        if self.search_options['search_value'] == '':
            err = 'search.py - __contsruct_url() - search needs a search value (job title)!'
            raise Exception(err)

        if self.search_options['job_salary_est'] != '':

            f1 = self.search_options['search_value']
            f2 = self.search_options['job_salary_est']

            query_job_salary = query_job_salary.format(f1, f2)

        else:
            query_job_salary = self.search_options['search_value']

        query_string = query_string + query_job_salary.replace(' ', '+').replace(',','%2c')


        #Note, if multiple searches are to be run from one search object, re-write these to use temp
        #strings rather than overwriting the format strings
        if self.search_options['job_type'] != '':
            query_job_type = query_job_type.format(self.search_options['job_type'])
            query_string = query_string + query_job_type

        if self.search_options['job_location'] != '':
            query_location = query_location.format(self.search_options['job_location'])
            query_string = query_string + query_location.replace(' ', '+').replace(',','%2C')

        else:
            err = 'search.py - __construct_url() - search needs a location!'
            raise Exception(err)

        if self.search_options['job_experience'] != '':
            query_exp_level = query_exp_level.format(self.search_options['job_experience'])
            query_string = query_string + query_exp_level

        url = url_form_0.format(query_string)

        #set the search options to the website url. There should probably be an option and a check
        #for this
        print('\nFinal Search URL: {}'.format(url))
        self.search_options['website_url'] = url

        

        return url
        
        
        
        
                
                
                
                
            
        


        
            
