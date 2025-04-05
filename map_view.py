# map_view.py

import pandas as pd
import folium
from folium.plugins import MarkerCluster

def generate_map():
    # Load Data
    parks_df = pd.read_csv("matched_national_parks.csv")
    ranking_df = pd.read_csv("AnnualParkRankingReport.csv", skiprows=3)

    # Data Preprocessing
    ranking_df["RecreationVisitors"] = ranking_df["Value"].str.replace(",", "").astype(int)
    ranking_df["FirstWord"] = ranking_df["ParkName"].str.split().str[0].str.lower()
    parks_df["FirstWord"] = parks_df["wiki_name"].str.split().str[0].str.lower()

    # Merge DataFrames
    merged_df = (
        pd.merge(parks_df, ranking_df, on="FirstWord", how="left")
        .sort_values("Rank")
        .drop_duplicates(subset="wiki_name")
    )

    #initializing the map
    us_map = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles="CartoDB positron")
    main_cluster = MarkerCluster(name="National Park Location").add_to(us_map)

    for _, row in merged_df.iterrows():
        try:
            lat = float(row["lat"])
            lon = float(row["lon"])
            name = row["wiki_name"]
            visitors = f"{row['RecreationVisitors']:,}" if pd.notnull(row["RecreationVisitors"]) else "N/A"
            rank = int(row["Rank"]) if pd.notnull(row["Rank"]) else "N/A"
            popup_html = f"<div style='width:300px'><b>{name}</b><br>Visitors: {visitors}<br>Rank: {rank}</div>"
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=350)
            ).add_to(main_cluster)
        except Exception as e:
            print(f"[Main Error] {row.get('wiki_name', 'Unknown')}: {e}")

    #adding campgrounds layer
    camp_df = pd.read_csv("campgrounds_data.csv")
    camp_layer = folium.FeatureGroup(name="Campgrounds")

    for _, row in camp_df.iterrows():
        try:
            lat, lon = float(row["lat"]), float(row["lon"])
            popup = f"<div style='width:300px'><b>{row['campground_name']}</b><br><i>{row['wiki_name']}</i><br>{row['description']}</div>"
            folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color="green", icon="cloud")).add_to(camp_layer)
        except Exception as e:
            print(f"[Camp Error] {row.get('campground_name', 'Unknown')}: {e}")

    camp_layer.add_to(us_map)

    # Adding Visitor Centers Layer
    vc_df = pd.read_csv("visitor_centers.csv")
    vc_layer = folium.FeatureGroup(name="Visitor Centers")

    for _, row in vc_df.iterrows():
        try:
            lat, lon = float(row["lat"]), float(row["lon"])
            hours = "<br>".join([
                f"{day.capitalize()}: {row[day]}" for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                if day in row
            ])
            popup = f"""
            <div style='width:300px'>
                <b>{row['name']}</b><br>
                <i>{row['wiki_name']}</i><br>
                {row['description']}<br><br>
                <a href="{row['directionsUrl']}" target="_blank">Directions</a><br><br>
                {hours}
            </div>
            """
            folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color="blue", icon="info-sign")).add_to(vc_layer)
        except Exception as e:
            print(f"[VC Error] {row.get('name', 'Unknown')}: {e}")

    vc_layer.add_to(us_map)

    #Adding Webcams Layer
    webcam_df = pd.read_csv("nps_webcams.csv")
    webcam_layer = folium.FeatureGroup(name="Webcams")

    for _, row in webcam_df.iterrows():
        try:
            lat, lon = float(row["lat"]), float(row["lon"])
            popup = f"""
            <div style='width:300px'>
                <b>{row['title']}</b><br>
                <i>{row['wiki_name']}</i><br>
                <a href="{row['url']}" target="_blank">Live Stream</a>
            </div>
            """
            folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color="red", icon="camera")).add_to(webcam_layer)
        except Exception as e:
            print(f"[Webcam Error] {row.get('title', 'Unknown')}: {e}")

    webcam_layer.add_to(us_map)

    # Layer Control
    folium.LayerControl().add_to(us_map)

    # Save the map
    us_map.save("national_parks_map_layers.html")
    print("Map Save to：national_parks_map_layers.html")
