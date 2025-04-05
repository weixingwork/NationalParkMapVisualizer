import pandas as pd
import requests

# load parkCode from matched_national_parks.csv
parks_df = pd.read_csv("matched_national_parks.csv")
sample_parks = parks_df[['wiki_name', 'parkCode']]  

API_KEY = '111'
alert_records = []

for _, row in sample_parks.iterrows():
    park_code = row['parkCode']
    wiki_name = row['wiki_name']
    
    url = f"https://developer.nps.gov/api/v1/alerts?parkCode={park_code}&api_key={API_KEY}"
    try:
        resp = requests.get(url)
        data = resp.json()

        if not data.get('data'): 
            print(f"No alerts for {wiki_name} ({park_code})")

        for alert in data.get('data', []):
            alert_records.append({
                'wiki_name': wiki_name,
                'parkCode': park_code,
                'title': alert.get('title'),
                'category': alert.get('category'),
                'description': alert.get('description'),
                'lastIndexedDate': alert.get('lastIndexedDate'),
                'url': alert.get('url'),
            })

    except Exception as e:
        alert_records.append({
            'wiki_name': wiki_name,
            'parkCode': park_code,
            'title': 'Error',
            'category': '',
            'description': str(e),
            'lastIndexedDate': '',
            'url': ''
        })

# Save the alerts to a CSV file
alerts_df = pd.DataFrame(alert_records)
alerts_df.to_csv("alert.csv", index=False)

print("Alerts 数据已保存到 alerts.csv")
