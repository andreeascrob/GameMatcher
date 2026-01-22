import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    dati = []
    
    # Apriamo il file CSV in lettura
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Trasformiamo ogni riga in un dizionario e la aggiungiamo alla lista
        for rows in csv_reader:
            dati.append(rows)

    # Scriviamo i dati in un file JSON
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(dati, json_file, indent=4, ensure_ascii=False)

# Esempio di utilizzo
csv_to_json('/home/andreea/GameMatcher/D3/Scraping/steam_top_100.csv', 'steam_top_100.json')