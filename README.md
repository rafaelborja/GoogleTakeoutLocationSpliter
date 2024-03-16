# Google Takeout Location History Splitter

This Python script splits your Google Takeout location history JSON file into separate files by year.

## Requirements

- Python 3.x

## Usage 
Run the script from the command line, providing the necessary arguments. Here is a basic example:

```
python location_history_splitter.py <input_file> --split_type <split_type> --simplify_output --time_threshold <time_threshold> --distance_threshold <distance_threshold> --debug
```

Replace `<input_file>` with the path to your Google Takeout location history JSON file. Adjust the `--split_type`, `--time_threshold`, and `--distance_threshold` arguments as needed.

### Arguments

- `input_file`: Path to the Google Takeout location history JSON file. (required)
- `--split_type`: How to split the location history file. Options are 'year', 'month', 'week', 'day', 'none'. Default is 'month'.
- `--simplify_output`: Simplify the output to only include timestamp, latitudeE7, and longitudeE7. (optional)
- `--time_threshold`: Time threshold in seconds to ignore subsequent location entries. (optional)
- `--distance_threshold`: Distance threshold in meters to ignore subsequent location entries. (optional)
- `--debug`: Enable debug logging. (optional)

## Example

```
python location_history_splitter.py "path/to/your/location_history.json" --split_type month --simplify_output --time_threshold 60 --distance_threshold 1000 --debug
```

This command will process the specified location history file, splitting it by month, simplifying the output, applying a time threshold of 60 seconds, a distance threshold of 1000 meters, and enabling debug logging.

## Output

The script will generate one or more JSON files containing the split and optionally simplified location data. Files are named using the format `location_history_<period>.json`.

The script will create separate JSON files for each year with locations, named in the format location_history_YEAR.json.

## License
This project is licensed under the Apache License 2.0. See the LICENSE file for more details.

## Acknowledgements
This script was created by Rafael de Medeiros Borja Gomes https://github.com/rafaelborja/
For any questions or issues, please open an issue on GitHub.
