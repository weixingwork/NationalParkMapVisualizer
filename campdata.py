import pandas as pd
import requests

def fetch_and_save_campground_data():
    parks_df = pd.read_csv("matched_national_parks.csv")
    sample_parks = parks_df[['wiki_name', 'parkCode']]

    API_KEY = '111'
    campground_records = []

    for _, row in sample_parks.iterrows():
        park_code = row['parkCode']
        wiki_name = row['wiki_name']

        url = f"https://developer.nps.gov/api/v1/campgrounds?parkCode={park_code}&api_key={API_KEY}"
        try:
            resp = requests.get(url)
            data = resp.json()

            if not data.get('data'):
                print(f"[No Campgrounds] {wiki_name} ({park_code})")

            for camp in data.get('data', []):
                operating_hours = camp.get('operatingHours', [])
                operating_description = operating_hours[0].get('description', '') if operating_hours else ''

                amenities = camp.get('amenities', {}).get('amenityDescription', [])
                amenities_text = ", ".join(amenities) if isinstance(amenities, list) else ''

                campsite_info = camp.get('campsites', {})
                total_sites = campsite_info.get('totalSites', '')

                campground_records.append({
                    'wiki_name': wiki_name,
                    'parkCode': park_code,
                    'campground_name': camp.get('name'),
                    'description': camp.get('description'),
                    'lat': camp.get('latitude'),
                    'lon': camp.get('longitude'),
                    'numberOfSitesReservable': total_sites,
                    'reservationInfo': camp.get('reservationInfo'),
                    'amenities': amenities_text,
                    'operatingHours': operating_description
                })

        except Exception as e:
            print(f"[Camp API Error] {wiki_name} ({park_code}): {str(e)}")

    camp_df = pd.DataFrame(campground_records)
    camp_df.to_csv("campgrounds_data.csv", index=False)
    print("Campgrounds data saved to campgrounds_data.csv")

if __name__ == "__main__":
    fetch_and_save_campground_data()
