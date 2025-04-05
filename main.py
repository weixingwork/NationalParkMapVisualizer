# main.py
# Main entry to generate park data and final map

from match_parks_nps import fetch_and_save_matched_parks
from campdata import fetch_and_save_campground_data
from Visitor_Centers import fetch_and_save_visitor_centers
from webcams import fetch_and_save_webcams
import map_view

def main():
    print("Step 1: Matching national parks and saving to matched_national_parks.csv")
    fetch_and_save_matched_parks()

    print("Step 2: Fetching campground data and saving to campgrounds_data.csv")
    fetch_and_save_campground_data()

    print("Step 3: Fetching visitor center data and saving to visitor_centers.csv")
    fetch_and_save_visitor_centers()

    print("Step 4: Fetching webcam data and saving to nps_webcams.csv")
    fetch_and_save_webcams()

    print("Step 5: Creating national parks map with all layers")
    map_view.generate_map()

if __name__ == "__main__":
    main()
