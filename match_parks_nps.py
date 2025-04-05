# match_parks_nps.py
#this code is used to match the names of national parks from a list with the data from the National Park Service (NPS) API. 
# The script retrieves park data from the NPS API, normalizes the names, and matches them with a predefined list of national park names. 
# The matched data is then saved to a CSV file.
#The reason for the match is because there are more than 63 national parks in the nps database, 
# and it includes some other parks totaling a few hundred, so we only need the 63 national parks we want. Here is the complete code:
import requests
import pandas as pd
import re
from get_park_names import get_national_park_names

def fetch_and_save_matched_parks():
    #loading names
    clean_names = get_national_park_names()

    #formatting names
    def normalize_name(name):
        cleaned = name.replace('–', '-').replace('—', '-').lower()
        return re.sub(r'[^a-z]', '', cleaned)

    #getting NPS data
    API_KEY = '111'
    nps_url = 'https://developer.nps.gov/api/v1/parks'
    params = {'limit': 500, 'api_key': API_KEY}
    response = requests.get(nps_url, params=params)
    data = response.json()['data']

    #match names
    matched_data = []
    for name in clean_names:
        norm_name = normalize_name(name)

        found = False
        for item in data:
            full_name = item.get('fullName', '')
            if norm_name in normalize_name(full_name):
                matched_data.append({
                    'wiki_name': name,
                    'nps_fullName': full_name,
                    'parkCode': item.get('parkCode', ''),
                    'states': item.get('states', ''),
                    'lat': item.get('latitude', ''),
                    'lon': item.get('longitude', ''),
                    'url': item.get('url', ''),
                })
                found = True
                break

        if not found:
            print(f"match false：{name}")

    #output matched data
    matched_df = pd.DataFrame(matched_data)
    print(f"\n sucessful match {len(matched_df)} / 63 national parks")
    matched_df.to_csv('matched_national_parks.csv', index=False)