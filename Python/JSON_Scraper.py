import json
import csv
import os
from pathlib import Path

# Directory where your JSON files are stored
json_directory_path = Path('.')
csv_file_path = 'output.csv'

# CSV headers
headers = ['URL', 'Blocked', 'Blocking Method']

# Function to process each JSON file and extract the data
def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        url = data.get('input', '')
        test_keys = data.get('test_keys', {})
        accessible = test_keys.get('accessible', '')
        blocking = test_keys.get('blocking', '')

        # Convert boolean to string for CSV output
        blocked = 'Yes' if not accessible and blocking else 'No'
        blocking_method = blocking if blocking else ''
        
        return [url, blocked, blocking_method]


# Write to CSV
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    # Walk through the directory and process each JSON file
    for file_name in os.listdir(json_directory_path):
        if file_name.endswith('.json'):
            try:
                row = process_json_file(json_directory_path / file_name)
                writer.writerow(row)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

print(f"Data extraction complete. CSV file created at {csv_file_path}")
