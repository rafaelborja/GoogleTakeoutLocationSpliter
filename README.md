# Google Takeout Location History Splitter

This Python script splits your Google Takeout location history JSON file into separate files by year.

## Requirements

- Python 3.x

## How to Use

1. Ensure you have Python installed on your computer. You can download Python [here](https://www.python.org/downloads/).

2. Place your Google Takeout location history JSON file in the same directory as the script, or note its path.

3. Open a terminal or command prompt.

4. Navigate to the directory containing the script.

Run the script with the following command, where `your_location_history.json` is the path to your Google Takeout location history JSON file:

```bash
python split_location_history.py your_location_history.json
```

The script will create separate JSON files for each year with locations, named in the format location_history_YEAR.json.

## License
This project is licensed under the Apache License 2.0. See the LICENSE file for more details.

## Acknowledgements
This script was created by Rafael de Medeiros Borja Gomes https://github.com/rafaelborja/
For any questions or issues, please open an issue on GitHub.
