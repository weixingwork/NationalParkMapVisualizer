import pandas as pd
import requests

API_KEY = '111'

def fetch_and_save_visitor_centers():
    parks_df = pd.read_csv("matched_national_parks.csv")
    sample_parks = parks_df[['wiki_name', 'parkCode']]
    visitor_centers = []

    for _, row in sample_parks.iterrows():
        park_code = row['parkCode']
        wiki_name = row['wiki_name']

        url = f"https://developer.nps.gov/api/v1/visitorcenters?parkCode={park_code}&api_key={API_KEY}"
        try:
            resp = requests.get(url)
            data = resp.json()

            if not data.get('data'):
                print(f"No visitor centers for {wiki_name} ({park_code})")

            for vc in data.get('data', []):
                hours = vc.get('operatingHours', [])
                std_hours = hours[0].get('standardHours', {}) if hours else {}

                visitor_centers.append({
                    'wiki_name': wiki_name,
                    'parkCode': park_code,
                    'name': vc.get('name'),
                    'lat': vc.get('latitude'),
                    'lon': vc.get('longitude'),
                    'description': vc.get('description'),
                    'directionsInfo': vc.get('directionsInfo'),
                    'directionsUrl': vc.get('directionsUrl'),
                    'url': vc.get('url'),
                    'monday': std_hours.get('monday', ''),
                    'tuesday': std_hours.get('tuesday', ''),
                    'wednesday': std_hours.get('wednesday', ''),
                    'thursday': std_hours.get('thursday', ''),
                    'friday': std_hours.get('friday', ''),
                    'saturday': std_hours.get('saturday', ''),
                    'sunday': std_hours.get('sunday', ''),
                })

        except Exception as e:
            print(f"Error for {wiki_name} ({park_code}): {str(e)}")

    visitor_df = pd.DataFrame(visitor_centers)
    visitor_df.to_csv("visitor_centers.csv", index=False)

    print("Visitor Center data saved to visitor_centers.csv")
