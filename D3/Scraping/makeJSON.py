import csv
import json
from pathlib import Path

def csv_to_json(csv_filename, json_filename):
    # Get the directory where the script is currently located
    base_path = Path(__file__).parent
    
    # Create full paths based on that directory
    csv_path = base_path / csv_filename
    json_path = base_path / json_filename
    
    dati = []
    
    if not csv_path.exists():
        print(f"Error: {csv_filename} not found in {base_path}")
        return

    with open(csv_path, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for rows in csv_reader:
            dati.append(rows)

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(dati, json_file, indent=4, ensure_ascii=False)
    
    print(f"Successfully converted {csv_filename} to {json_filename}")

# Usage: Now you only need the filenames
csv_to_json('steam_top_100.csv', 'steam_top_100.json')