#This script initializes the zyberkatz db upon first run.

import sqlite3
import os.path
import json

db_names = {'db_name':'',
            'global_listing_table':'',
            'global_search_table':'',
            'global_junction_table':''}

#Check if the db settings file exits. If not, create it
if !os.path.isfile('./db_settings.txt'):
    
    db_file = open('db_settings.txt', 'w')
    
    db_file.write('db_name:zyberkatz.db\n')
    db_file.write('global_listing_table_name:listing\n')
    db_file.write('global_search_table_name:search\n')
    db_file.write('global_junction_table_name:junction\n')

else:
    
