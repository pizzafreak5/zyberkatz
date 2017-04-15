import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import hashlib
import re
from datetime import datetime, timedelta #time

class scraper:
    def __init__(self, settings, db_cursor, table):
        self.visited_links = []                              #Used to store visited links
        self.nav_links = []
        self.job_links = []
        self.next_count = 0
        
        if 'website_url' not in settings:
            raise Exception("Missing website url")
        self.url = settings['website_url']
        
        if 'div_class_links' not in settings:
            raise Exception("div class for links to more results is missing")
        self.div_link_class = settings['div_class_links']
        
        if 'div_class_listings' not in settings:
            raise Exception('div class for listings is missing')
        self.div_class_listings = settings['div_class_listings']
        
        if 'company_name_tag' not in settings:
            raise Exception('missing tags for company name')
        self.company_name_tag = settings['company_name_tag']
        
        if 'company_name_attrs' not in settings:
            raise Exception('missing attrs dict for company name')
        self.company_name_attrs = settings['company_name_attrs']
        
        if 'job_loc_tag' not in settings:
            raise Exception('missing tags for job location')
        self.job_loc_tag = settings['job_loc_tag']
        
        if 'job_loc_attrs' not in settings:
            raise Exception('missing attrs dict for job location')
        self.job_loc_attrs = settings['job_loc_attrs']
        
        if 'time_posted_tag' not in settings:
            raise Exception('missing tags for time posted')
        self.time_posted_tag = settings['time_posted_tag']
        
        if 'time_posted_attrs' not in settings:
            raise Exception('missing attrs dict for time posted')
        self.time_posted_attrs = settings['time_posted_attrs']
        
        if 'job_desc_tag' not in settings:
            raise Exception('missing tags for job description')
        self.job_desc_tag = settings['job_desc_tag']
        
        if 'job_desc_attrs' not in settings:
            raise Exception('missing attrs dict for job description')
        self.job_desc_attrs = settings['job_desc_attrs']
        
        if 'job_title_tag' not in settings:
            raise Exception('missing job title tag')
        self.job_title_tag = settings['job_title_tag']
        
        if 'https' not in settings:
            self.https = 'http://'
        else:
            self.https = settings['https']
            
        if 'limit' not in settings:
            self.limit = 1
        else:
            self.limit = int(settings['limit'])
            
        if 'headers' not in settings:
            self.headers = None
        else:
            self.headers = settings['headers']
            
        if 'experience' not in settings:
            self.experience = ""
        else:
            self.experience = settings['experience']
            
        if 'salary_est' not in settings:
            self.salary_est = ""
        else:
            self.salary_est = settings['salary_est']
            
        if 'job_type' not in settings:
            self.job_type = ""
        else:
            self.job_type = settings['job_type']
        
        self.cursor = db_cursor
        self.table = table
        self.domain = urlparse(self.url).hostname
        
        
    def next_results(self, url, get):
        soup = BeautifulSoup(get.text, 'lxml')
        results = soup.find_all('div', attrs={'class':self.div_link_class})
        
        nav_links = []
        
        for result in results:
            links = result.findAll('a')
            for link in links:
                url = self.https + self.domain + link['href']
                if url not in nav_links:
                    nav_links.append(url)

        return nav_links
    
    def convert_time_posted(self, time):
        digit = time.split(' ')       
        today = datetime.now()
        digit[0] = digit[0].replace("+", "")
        #subtract it as days
        if 'day' in time:
            today = today - timedelta(days=int(digit[0]))
        #subtract it as hours
        elif 'hour' in time:
            today = today - timedelta(hours=int(digit[0]))
        
        return today
    
    def process_content(self, get, url):
        soup = BeautifulSoup(get.text, 'lxml')    
        
        for i in range(len(self.div_class_listings)):
            listings = soup.find_all('div', attrs={'class':self.div_class_listings[i]})
            for listing in listings:
                company_name = listing.find(self.company_name_tag, self.company_name_attrs)
                if company_name != None:
                    company_name = (company_name.text).strip()
                else:
                    company_name = ""
                
                job_title = listing.find(self.job_title_tag)           
                if job_title != None:
                    job_title = job_title.text
                else:
                    job_title = ""
                
                location = listing.find(self.job_loc_tag, self.job_loc_attrs)
                if location != None:
                    location = location.text
                else:
                    location = ""
                
                job_desc = listing.find(self.job_desc_tag, self.job_desc_attrs)
                if job_desc != None:
                    job_desc = job_desc.text
                else:
                    job_desc = ""
                
                job_link = str(listing.find('a')['href'])
                job_link = self.domain + job_link
                
                time_posted = listing.find(self.time_posted_tag, self.time_posted_attrs)
                if time_posted != None:
                    time_posted = time_posted.text
                    time_posted = self.convert_time_posted(time_posted)
                else:
                    time_posted = "None"
                
                
                #prepare url
                job_link = self.https + job_link
                
                #Job page text
                if self.headers != None:
                    get = requests.get(job_link, headers = self.headers)
                else:
                    get = requests.get(job_link)
            
                job_listing = BeautifulSoup(get.text, "lxml")
                [terms.extract() for terms in job_listing(['style', 'script', '[document]', 'head', 'title'])]
                job_listing_str = job_listing.getText()
                job_listing_str = re.sub('\s+', ' ', job_listing_str).strip()
                                
                #used for key
                hash_val = hashlib.sha256((job_title+job_desc).encode('utf-8')).hexdigest()
                
                #Check for Redudant Entries
                query = 'SELECT * FROM ' + self.table + ' WHERE hash_val=?'
                self.cursor.execute(query, (hash_val,) )
                if self.cursor.fetchone() != None:
                    return                                  #DUPLICATE ENTRY
                
                #Add to database
                experience = self.experience
                salary_est = self.salary_est
                job_type = self.job_type
                data = (hash_val, company_name, time_posted, job_title, job_desc, location, experience, salary_est, job_type, job_link, job_listing_str)
                query = 'INSERT INTO ' + self.table + ' (hash_val,company,time_posted,job_title,job_desc,job_loc,job_exp,salary_est,job_type,link,job_text) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
                self.cursor.execute(query, data)
                
                ''' Write to file
                filename = url.replace(":", "").replace("/", "").replace("?", "").replace("%", "").replace("&", "")
                file = open(filename+".html", "wb")
                file.write(("<b>JOB LISTING:</b><br/>").encode("utf-8"))
                job_link = 'http://' + job_link + '<br/>'
                file.write(("Company: ").encode("utf-8"))
                file.write((company_name + "<br/>").encode("utf-8"))
                file.write(("Job Title: ").encode("utf-8"))
                file.write((job_title + "<br/>").encode("utf-8"))
                file.write(("Location:" + location + "<br/>").encode('utf-8'))
                file.write(("Description:<br/>").encode("utf-8"))
                file.write((job_desc + "<br />").encode("utf-8"))
                file.write(("Time posted:" + time_posted).encode("utf-8"))
                file.write(("<b>LINK TO JOB POSTING:</b><br/>").encode("utf-8"))
                file.write((job_link + "<br/>").encode("utf-8"))
                #'''   
                
                
        
    
    def scrape(self, url):
        if url in self.visited_links:           #Avoid visiting the same page
            return
        
        self.next_count += 1                    #It's time to stop
        if self.limit < self.next_count:
            return
            
        if self.headers == None:
            get = requests.get(url)
        else:
            get = requests.get(url, headers = self.headers)
        if get.status_code != 200:              #Failed to connect to site
            error = "Expected status code 200, got "
            error += str(get.status_code)
            print (error)
            return
        
        #mark this url as visited
        self.visited_links.append(url)          

        #Process the content
        self.process_content(get, url)
        
        #Grab the next set of links
        nav_links = self.next_results(url, get)
        if nav_links != None:
            for i in range(len(nav_links)):
                self.scrape(nav_links[i])
 
                
                
        
        
        
        
def generate_url(url):
    dict_string = 'parameter'                   #parameter in url is defined in the dict as
    if 'website_url' not in url:
        raise Exception("Failed to find website_url in parameter passed in")
    term = url['website_url'].count('{}')       #website url, get the amount of parameters
    website_url = url['website_url']            #get the website url
        
    for i in range(term):                       #for all the parameters
        current_dict = dict_string + str(i)     #change parameter to the form parameterINT
        if current_dict not in url:             #check to make sure the parameter is defined in the dict
            error = "Failed to find the matching term in the dictionary for "
            error += current_dict
            raise Exception(error)
        website_url = website_url.replace('{}', url[current_dict], 1)  #replace the current parameter with its corresponding value
    
    return website_url

