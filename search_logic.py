import search
import db
import sqlite3

#run_search will take a job title and location
#and iterate through other possible search values
#such as job type and salary
#Precondition:
#The database and all tables must be initialized
#Postcondition:
#The database tables search, listing, and junction
#have been popluated with new entries
def run_search(job_title, location, search_title):

        datab = sqlite3.connect(db.information['db_name'])
        db_cursor = datab.cursor()

        #Listing attribute string
        q = '''
UPDATE listing SET job_type = '{}', job_exp = '{}', salary_est = '{}'
WHERE hash_val = (SELECT hash_val FROM junction WHERE search_hash = '{}')
'''

        #180 searches per user search! Lets do this.
        job_exp = ['entry_level','mid_level','senior_level']
        job_salaries = ['$14,000','$30,000','$50,000','$70,000',
                        '$90,000']
        job_types = ['fulltime', 'contract', 'internship', 'temporary',
                    'parttime', 'commission']

        for xp in job_exp:
                for sal in job_salaries:
                        for typ in job_types:
                                search_options = {'search_title':'',
                                                  'search_value':'',
                                                  'job_location':'',
                                                  'job_salary_est':'',
                                                  'limit':'',
                                                  'job_type':'',
                                                  'job_experience':'',
                                                  'website_url':'',
                                                  'global_db_name':'zyber.db'}
                                search_options['search_title'] = search_title
                                search_options['search_value'] = job_title
                                search_options['job_location'] = location
                                search_options['job_salary_est'] = sal
                                search_options['job_type'] = typ
                                search_options['job_experience'] = xp

                                search_ob = search.Search(search_options)
                                search_ob.search()

                                db_cursor.execute(q.format(typ, xp, sal, search_ob.search_hash))

                                datab.commit()

        

def get_jobs_with_field(field, value):
        
        q = '''
SELECT {} 
FROM listing 
WHERE hash_val IN
(SELECT hash_val FROM junction
WHERE search_hash IN
(SELECT search_hash FROM search
WHERE job_exp = 'mid_level'));'''

#Time strings come in as MM-DD-YY
def jobs_v_time(time_start, time_end, sal_min, sal_max, job_type_set, job_exp_set):

        #parse the time strings
        start_time = time_start.split('-')
        end_time - time_end.split('-')
        #Get job listings within time range

        
def pie_graph_data(search_title, search_date, attribute, attribute_values):

        q = '''
SELECT {} FROM search
WHERE search_title = '{}'
AND search_date = '{}';'''

        
        
