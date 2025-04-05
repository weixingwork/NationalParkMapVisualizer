# get_park_names.py

import pandas as pd
import re

def get_national_park_names():
    url = 'https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States'
    tables = pd.read_html(url)

    for table in tables:
        if 'Name' in table.columns and 'Location' in table.columns:
            park_table = table
            break

    # Clean the column names
    park_table.columns = [col.strip().split('[')[0] for col in park_table.columns]
    raw_names = park_table['Name'].tolist()
    clean_names = [re.sub(r'[†‡*]', '', name).strip() for name in raw_names]

    return clean_names
#print (len(get_national_park_names()))