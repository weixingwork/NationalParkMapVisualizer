import pandas as pd
import requests

# LOad parkCode
parks_df = pd.read_csv("matched_national_parks.csv")
sample_parks = parks_df[['wiki_name', 'parkCode']]

API_KEY = '111'
things_to_do = []

for _, row in sample_parks.iterrows():
    park_code = row['parkCode']
    wiki_name = row['wiki_name']

    url = f"https://developer.nps.gov/api/v1/thingstodo?parkCode={park_code}&api_key={API_KEY}"
    try:
        resp = requests.get(url)
        data = resp.json()

        if not data.get('data'):
            print(f"No activities for {wiki_name} ({park_code})")

        for item in data.get('data', []):
            activity_list = item.get('activities', [])
            activity_tags = ", ".join([a['name'] for a in activity_list])

            things_to_do.append({
                'wiki_name': wiki_name,
                'parkCode': park_code,
                'title': item.get('title'),
                'shortDescription': item.get('shortDescription'),
                'location': item.get('location'),
                'url': item.get('url'),
                'duration': item.get('duration'),
                'activity_tags': activity_tags
            })

    except Exception as e:
        print(f"Error for {wiki_name} ({park_code}): {str(e)}")

# save to csv
things_df = pd.DataFrame(things_to_do)
things_df.to_csv("things_to_do.csv", index=False)

print("thing to do save to things_to_do.csv")
