import search
import db

#run_search will take a job title and location
#and iterate through other possible search values
#such as job type and salary
#Precondition:
#The database and all tables must be initialized
#Postcondition:
#The database tables search, listing, and junction
#have been popluated with new entries
def run_search(job_title, location, search_title):

        #180 searches per user search! Lets do this.
        job_exp = ['entry_level','mid_level','senior_level']
        job_salaries = ['$14,000','$20,000','$30,000','$40,000',
                        '$50,000','$60,000','$70,000','$80,000',
                        '$90,000','$100,000']
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

        


        
        

        
