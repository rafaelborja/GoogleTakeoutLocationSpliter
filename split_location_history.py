import json
from datetime import datetime

def split_location_history_by_year(input_file):
    # Load the JSON data from the Google Takeout location history file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check if 'locations' key exists in the data
    if 'locations' not in data:
        print("The provided file does not have a 'locations' key.")
        return

    locations_by_year = {}

    # Iterate through each location in the location history
    for location in data['locations']:
        # Extract the timestamp from the location data
        timestamp_ms = int(location['timestampMs'])
        # Convert timestamp to a datetime object
        date = datetime.fromtimestamp(timestamp_ms / 1000.0)
        year = date.year

        # Add the location to the respective year's list
        if year not in locations_by_year:
            locations_by_year[year] = []
        locations_by_year[year].append(location)

    # Create separate JSON files for each year
    for year, locations in locations_by_year.items():
        output_file = f'location_history_{year}.json'
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump({"locations": locations}, file, ensure_ascii=False, indent=4)
            print(f"Saved {len(locations)} locations to {output_file}")

# Replace 'your_location_history.json' with the path to your Google Takeout location history JSON file
split_location_history_by_year('your_location_history.json')
