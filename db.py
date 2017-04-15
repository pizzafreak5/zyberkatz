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
CREATE TABLE {}
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
CREATE TABLE {}
(
search_hash	TEXT PRIMARY KEY,
search_title	TEXT,
search_date	TEXT,
search_value	TEXT,
search_loc	TEXT,
job_type	TEXT,
job_exp		TEXT,
job_salary_min	TEXT
);
'''
create_junction_table = '''
CREATE TABLE {}
(
hash_val	TEXT FOREIGN KEY NOT NULL,
search_hash	TEXT FOREIGN KEY NOT NULL,
);
'''

db_names = {'db_name':'zyberkatz.db',
            'global_listing_table':'listing',
            'global_search_table':'search',
            'global_junction_table':'junction'}

db_hash_string = db_names['db_name'] + db_names['global_listing_table'] + db_names['global_search_table'] + db_names['global_junction_table']
db_settings_hashed = hashlib.sha256((db_hash_string).encode('utf-8')).hexdigest()

db_names['hash'] = db_settings_hashed

#Check if the db settings file exits. If not, create it
if !os.path.isfile('./db_settings.txt'):
    
    db_file = open('db_settings.txt', 'w')
    
    db_file.write(json.dumps(db_names))

    #In this case, this is the first startup, so the database
    #needs to be initialized
    db = sql.connect(db_names['db_name'])
    db_cursor = db.cursor()

    listing_q = create_listing_table.format(db_names['global_listing_table'])
    search_q = create_search_table.format(db_names['global_search_table'])
    junction_q = create_junction_table.format(db_names['global_junction_table'])

    db.execute(listing_q)
    db.execute(search_q)
    db.execute(junction_q)

    db.commit()

    db_file.close()

else:
    db_file = db_file = open('db_settings.txt', 'r')
    db_names = json.load(db_file)
    db_file.close
    
#Check to see if the settings match the hash. If they don't
#the settings have most likely been edited and the db needs
#to be re-initialized

check_hash = db_names['db_name'] + db_names['global_listing_table'] + db_names['global_search_table'] + db_names['global_junction_table']
db_settings_hashed = hashlib.sha256((db_hash_string).encode('utf-8')).hexdigest()

if db_settings_hashed != db_names[hash]:
    db = sql.connect(db_names['db_name'])
    db_cursor = db.cursor()

    listing_q = create_listing_table.format(db_names['global_listing_table'])
    search_q = create_search_table.format(db_names['global_search_table'])
    junction_q = create_junction_table.format(db_names['global_junction_table'])

    db.execute(listing_q)
    db.execute(search_q)
    db.execute(junction_q)

    db.commit()
