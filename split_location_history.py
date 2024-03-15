import json
import argparse
from datetime import datetime

def split_location_history_by_year(input_file):
    # Load the JSON data from the Google Takeout location history file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if 'locations' not in data:
        print("The provided file does not have a 'locations' key.")
        return

    locations_by_year = {}

    for location in data['locations']:
        timestamp_ms = int(location['timestampMs'])
        date = datetime.fromtimestamp(timestamp_ms / 1000.0)
        year = date.year

        if year not in locations_by_year:
            locations_by_year[year] = []
        locations_by_year[year].append(location)

    for year, locations in locations_by_year.items():
        output_file = f'location_history_{year}.json'
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump({"locations": locations}, file, ensure_ascii=False, indent=4)
            print(f"Saved {len(locations)} locations to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Split Google Takeout location history JSON file by year.")
    parser.add_argument("input_file", help="Path to the Google Takeout location history JSON file.")
    
    args = parser.parse_args()

    split_location_history_by_year(args.input_file)

if __name__ == "__main__":
    main()
