import json
import argparse
from datetime import datetime
import logging


def calculate_distance(location1, location2):
    # Simplified distance calculation
    lat_diff = abs(location1['latitudeE7'] - location2['latitudeE7'])
    lon_diff = abs(location1['longitudeE7'] - location2['longitudeE7'])
    return lat_diff, lon_diff


def process_locations(location, split_type, simplify_output, prev_location=None, time_threshold=None,
                      distance_threshold=None):
    # Parse the timestamp
    timestamp = str_2_timestamp(location['timestamp'])

    if split_type == "year":
        return location, timestamp.year
    elif split_type == "month":
        return location, timestamp.strftime('%Y-%m')
    elif split_type == "week":
        return location, timestamp.strftime('%Y-%U')
    elif split_type == "day":
        return location, timestamp.strftime('%Y-%m-%d')
    elif split_type == "none":
        return location, timestamp.strftime('')
    else:
        raise ValueError("Invalid split type. Choose from 'year', 'month', 'week', or 'day'.")


def should_ignore_location(current_location, previous_location, time_threshold, distance_threshold):
    if not previous_location:
        return False

    current_timestamp = str_2_timestamp(current_location['timestamp'])
    previous_timestamp = str_2_timestamp(previous_location['timestamp'])

    # Check time threshold
    if time_threshold is not None and ((current_timestamp - previous_timestamp).total_seconds() < time_threshold):
        logging.debug("Ignoring location due to time: current_timestamp: %s, previous_timestamp: %s ", current_timestamp, previous_timestamp)
        return True

    # Check distance threshold
    lat_diff, lon_diff = calculate_distance(current_location, previous_location)
    if distance_threshold is not None and (lat_diff <= distance_threshold * 90 or lon_diff <= distance_threshold * 98):
        logging.debug("Ignoring location due do distance Threshold: lat_diff: %s, lon_diff: %s ", lat_diff, lon_diff)
        return True

    return False


def str_2_timestamp(str_timestamp):
    try:
        return datetime.strptime(str_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    except Exception as e:
        return datetime.strptime(str_timestamp, '%Y-%m-%dT%H:%M:%SZ')


def split_location_history(input_file, split_type, simplify_output, time_threshold, distance_threshold):
    print(f"Opening the file: {input_file}")

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        return

    if 'locations' not in data:
        print(
            "The provided file does not have a 'locations' key. Please provide a valid Google Takeout location "
            "history JSON file.")
        return

    locations_by_period = {}
    ignored_count = 0
    total_ignored = 0
    print("Processing location data...")

    previous_location = None
    for location in data['locations']:
        try:
            if simplify_output:
                location = {
                    "timestamp": location['timestamp'],
                    "latitudeE7": location['latitudeE7'],
                    "longitudeE7": location['longitudeE7']
                }

            if time_threshold is not None or distance_threshold is not None:
                if should_ignore_location(location, previous_location, time_threshold, distance_threshold):
                    ignored_count += 1
                    logging.debug("Ignored location due to threshold constraints: %s", location['timestamp'])
                    continue

            location, period = process_locations(location, split_type, simplify_output, previous_location,
                                                 time_threshold, distance_threshold)
            if period not in locations_by_period:
                locations_by_period[period] = []
                print(f"Processing period: {period}")
            locations_by_period[period].append(location)
            previous_location = location
        except Exception as e:
            print(f"An error occurred while extracting data for location {location}: {e}")

    print(f"Splitting location data by {split_type}...")

    for period, locations in locations_by_period.items():
        output_file = f'location_history_{period}.json'
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump({"locations": locations}, file, ensure_ascii=False, indent=4)
                print(
                    f"Successfully saved {len(locations)} locations to {output_file}. Ignored {ignored_count} locations.")
                total_ignored += ignored_count
                ignored_count = 0  # Reset for next period
        except Exception as e:
            print(f"An error occurred while saving the file {output_file}: {e}")

    print(f"Total ignored locations due to thresholds: {total_ignored}")


def main():
    parser = argparse.ArgumentParser(description="Split Google Takeout location history JSON file by specified period.")
    parser.add_argument("input_file", help="Path to the Google Takeout location history JSON file.")
    parser.add_argument("--split_type", choices=["year", "month", "week", "day", "none"], default="month",
                        help="How to split the location history file. Options are 'year', 'month', 'week', or 'day'. "
                             "Default is 'month'.")
    parser.add_argument("--simplify_output", action="store_true",
                        help="Simplify the output to only include timestamp, latitudeE7, and longitudeE7.")
    parser.add_argument("--time_threshold", type=int, default=None,
                        help="Time threshold in seconds to ignore subsequent location entries.")
    parser.add_argument("--distance_threshold", type=int, default=None,
                        help="Distance threshold in meters to ignore subsequent location entries.")
    parser.add_argument("--single_file", action="store_true",
                        help="Generates a single output file")

    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logging.")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    split_location_history(args.input_file, args.split_type, args.simplify_output, args.time_threshold,
                           args.distance_threshold)


if __name__ == "__main__":
    main()
