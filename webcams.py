# webcams.py

import pandas as pd
import requests

API_KEY = '111'

def fetch_and_save_webcams():
    # load parkCode
    parks_df = pd.read_csv("matched_national_parks.csv")
    sample_parks = parks_df[['wiki_name', 'parkCode']]

    webcam_data = []

    for _, row in sample_parks.iterrows():
        park_code = row['parkCode']
        wiki_name = row['wiki_name']

        url = f"https://developer.nps.gov/api/v1/webcams?parkCode={park_code}&api_key={API_KEY}"
        try:
            resp = requests.get(url)
            data = resp.json()

            if not data.get('data'):
                print(f"No webcams for {wiki_name} ({park_code})")

            for cam in data.get('data', []):
                images = cam.get('images', [])
                first_image = images[0].get('url') if images else ''

                webcam_data.append({
                    'wiki_name': wiki_name,
                    'parkCode': park_code,
                    'title': cam.get('title'),
                    'status': cam.get('status'),
                    'url': cam.get('url'),
                    'lat': cam.get('latitude'),
                    'lon': cam.get('longitude'),
                    'first_image': first_image
                })

        except Exception as e:
            print(f"Error for {wiki_name} ({park_code}): {str(e)}")

    # save to csv
    webcam_df = pd.DataFrame(webcam_data)
    webcam_df.to_csv("nps_webcams.csv", index=False)

    print("camra info save to nps_webcams.csv")
