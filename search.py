import scraper
import json
import sqlite3
import datetime
import hashlib

class Search:

    def __init__(self, filename, search_options):

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

        try:
            file = open(filename, 'r')
            self.options = json.load(file)
            file.close()
        except:
            err = 'search.py - could not read file {}'.format(filename)
            raise Exception(err)

        #check for options passed in

        for key in self.search_options:
            if key in search_options:
                self.search_options[key] = search_options[key]
        

    def set_search_option(key, option):

        if key in search_options():
            self.search_options[key] = option
        else:
            err = 'search.py - set_search_option() - key {} is not a valid option key'.format(key)
        

    #How to call:  
    def search():

        #---------------
        #DB SETUP
        #---------------
        db = sqlite3.connect(self.search_options['global_db_name']) #Connect to the project database
        db_cursor = db.cursor()

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

        #Set options in scraper to options in search
        for option in self.search_options:
            if option in settings:
                settings[option] = self.search_options[settings]

        #---------------
        #RUN SCRAPER
        #---------------
        search_scraper = scraper.scraper(settings, db_cursor, 'temporary')
        search_scraper.scrape(search_scraper.url)

        #save changes to db
        db.commit()

        #---------------
        #APPEND TO SEARCH TABLE
        #---------------
        #Note: Consider changing this to UTC time.
        search_date = str(datetime.datetime.today())

        search_value = self.search_options['search_value']
        search_title = self.search_options['search_title']
        search_loc = self.search_options['job_location']
        search_sal = self.search_options['job_salary_est']
        search_exp = self.search_options['job_experience']
        search_type = self.search_options['job_type']
        
        hash_string = search_date + search_value + search_title + search_loc + search_sal + search_exp + search_type
        
        search_hash = hashlib.sha256((hash_string).encode('utf-8')).hexdigest()
        
        #Create the val string
        
        
        
        q = 'INSERT INTO {} VALUES ({});'
        

        #---------------
        #APPEND TO LISTING TABLE
        #---------------

        #append the new rows onto the global listing table
        q = 'SELECT * FROM listings WHERE hash_val NOT IN {};'.format(self.search_options['global_listings_table'])
        temp_data = db_cursor.execute(q)
        append_string = 'INSERT INTO {} VALUES({})'

        for row in temp_data:

            #Create the values string for each row
            values_string = ''
            for entry in row:

                #In order to get a value string that looks like
                # a, b, c, d
                #concatinate the first value without a comma
                if values_string == '':
                    values_string = str(entry)
                else:
                    values_string = values_string + ', ' + str(entry)

            insert_string = append_string.format(self.search_options, values_string)

        #
        

        

    #Returns the url to search
    def __construct_url():

        url_form_0 = 'https://www.indeed.com/jobs?q={}'
        url_form_1 = 'https://www.indeed.com/q-{}-{}-l-{}-jobs.html'#attempt to not use

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

        query_string.append(query_job_salary)


        #Note, if multiple searches are to be run from one search object, re-write these to use temp
        #strings rather than overwriting the format strings
        if self.search_options['job_type'] != '':
            query_job_type = query_job_type.format(self.search_options['job_type'])
            query_string.append(query_job_type)

        if self.search_options['location'] != '':
            query_location = query_location.format(self.search_options['job_location'])
            query_string.append(query_location)

        else:
            err = 'search.py - __construct_url() - search needs a location!'
            raise Exception(err)

        if self.search_options['job_experience'] != '':
            query_exp_level = query_exp_level.format(self.search_options['job_experience'])
            query_string.append(query_job_type)

        url = url_form_0.format(query_string)

        #set the search options to the website url. There should probably be an option and a check
        #for this
        print('\nFinal Search URL: {}'.format(url))
        self.search_options['website_url'] = url

        return url
        
        
        
        
                
                
                
                
            
        


        
            
