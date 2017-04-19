import search
import db
import sqlite3
import matplotlib
matplotlib.use("TkAgg")     # Needed so that tkinter doesn't crash
from matplotlib import pyplot as plt

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
        oldq = '''
UPDATE listing SET job_exp = '{}', job_type = '{}', salary_est = '{}'
WHERE hash_val = (SELECT hash_val FROM junction WHERE search_hash = '{}')
'''

        q = '''
UPDATE listing SET job_exp = '{}', job_type = '{}', salary_est = '{}' 
WHERE hash_val IN (SELECT hash_val FROM junction 
WHERE search_hash = '{}')
'''

        #180 searches per user search! Lets do this.
        job_exp = ['entry_level','mid_level','senior_level']
        job_salaries = ['$14,000','$30,000','$50,000','$70,000',
                        '$90,000']
        job_types = ['fulltime', 'contract', 'internship', 'temporary',
                    'parttime', 'commission']

        for sal in job_salaries:
                for typ in job_types:
                        for xp in job_exp:
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

                                db_cursor.execute(q.format(xp, typ, sal, search_ob.search_hash))
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
##########################################################

        new_job_exp_info = [0,0,0]   # each job exp is a index value
        state = "CO"        # casual variable

        for row in db_cursor.execute('SELECT job_exp FROM search WHERE job_loc LIKE "%'+state+'%"'):

            row_info = []
            for i in range(len(row)):
                if (row[i] == 'entry_level'):
                    temp = new_job_exp_info[0]
                    new_job_exp_info[0]= temp+1
                elif(row[i] == 'mid_level'):
                    temp = new_job_exp_info[1]
                    new_job_exp_info[1] = temp + 1
                elif(row[i] == 'senior_level'):
                    temp = new_job_exp_info[2]
                    new_job_exp_info[2] = temp + 1

        print (new_job_exp_info)
        #########################################################

        new_job_type_info = [0,0,0,0,0,0]   # each job type is a index value
        state = "CO"                        # casual variable

        for row in db_cursor.execute('SELECT job_type FROM search WHERE job_loc LIKE "%'+state+'%"'):

            row_info = []
            for i in range(len(row)):
                if (row[i] == 'fulltime'):
                    temp = new_job_type_info[0]
                    new_job_exp_info[0]= temp+1
                elif(row[i] == 'contract'):
                    temp = new_job_type_info[1]
                    new_job_exp_info[1] = temp + 1
                elif(row[i] == 'internship'):
                    temp = new_job_type_info[2]
                    new_job_exp_info[2] = temp + 1
                elif (row[i] == 'temporary'):
                    temp = new_job_type_info[3]
                    new_job_exp_info[3]= temp+1
                elif(row[i] == 'parttime'):
                    temp = new_job_type_info[4]
                    new_job_exp_info[4] = temp + 1
                elif(row[i] == 'commission'):
                    temp = new_job_type_info[5]
                    new_job_exp_info[5] = temp + 1


        print (new_job_type_info)

        #########################################################
        job_exp = ['entry_level', 'mid_level', 'senior_level']
        slices02 = [7,2,13]
        plt.pie(slices02,
                labels=job_exp,
                startangle=90,
                shadow=True,
                explode=(0,0.1,0),
                autopct= '%1.1f%%')
        plt.title('job_exp Pie Graph\nCheck it out')
        plt.legend()
        plt.show()

        # job_types = ['fulltime', 'contract', 'internship', 'temporary',
        #              'parttime', 'commission']
        # slices01 = [7,2,13,34,40,10]
        # plt.pie(slices01,
        #         labels=job_types,
        #         startangle=90,
        #         shadow=True,
        #         explode=(0,0.1,0,0,0,0),
        #         autopct= '%1.1f%%')
        # plt.title('job_types Pie Graph\nCheck it out')
        # plt.legend()
        # plt.show()
