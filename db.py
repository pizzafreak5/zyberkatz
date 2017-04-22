#This script initializes the zyberkatz db upon first run,
#and re-initialized if the settings have been changed.

#To retrieve database names from this script, use the code:
#import db
#db.db_names['example_name']
#or
#db.db_names.example_name

import sqlite3 as sql
import os.path
import json
import hashlib

create_listing_table = '''
CREATE TABLE if not exists listing
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
'''
create_search_table = '''
CREATE TABLE if not exists search
(
search_hash	TEXT PRIMARY KEY,
search_title	TEXT,
search_date	TEXT,
search_value	TEXT,
search_loc	TEXT,
job_type       TEXT,
job_exp		TEXT,
job_salary_min	TEXT
);
'''

create_junction_table = '''
CREATE TABLE if not exists junction
(
hash_val       TEXT,
search_hash    TEXT,
FOREIGN KEY(hash_val) REFERENCES listing(hash_val),
FOREIGN KEY(search_hash) REFERENCES search(search_hash)
);
'''

create_der_search_table = '''
CREATE TABLE if not exists der_search
(

);
'''

create_junction2_table = '''
CREATE TABLE if not exists 
(

);
'''



#If there is different values open them, otherwise default and then write to file the default
settings_file = open('db_settings.json', 'w+')
try:
    information = json.load(settings_file)
    
except:
    information = {'db_name':'zyber.db'}

settings_file.seek(0)
write_string = json.dumps(information)
settings_file.write(write_string)
settings_file.truncate()
settings_file.close()

#Create a database and the necessary tables needed
db = sql.connect(information['db_name'])
db.execute(create_listing_table)
db.execute(create_search_table)
db.execute(create_junction_table)   

