import json
import re
import os

# Lista dei file da processare
files_to_process = ['cpu_data.json', 'gpu_data.json', 'hardware_data.json']

def normalize_hardware_name(name):
    """
    Funzione per pulire e normalizzare i nomi hardware.
    """
    if not isinstance(name, str):
        return ""
    
    original_name = name
    
    # 1. Rimuove la frequenza alla fine (es. " @ 3.33GHz", " @ 2.40GHz")
    name = re.sub(r'\s*@\s*\d+(\.\d+)?\s*GHz.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*@\s*\d+(\.\d+)?\s*MHz.*', '', name, flags=re.IGNORECASE)

    # 2. Rimuove prefissi di memoria comuni nelle GPU (es. "256MB DDR", "512MB")
    name = re.sub(r'^\d+\s*MB\s+(?:DDR\s+)?', '', name, flags=re.IGNORECASE)
    name = re.sub(r'^\d+\s*GB\s+(?:DDR\s+)?', '', name, flags=re.IGNORECASE)

    # 3. Rimuove diciture generiche o ridondanti se necessario (opzionale)
    # name = name.replace("Dual-Core", "").replace("Quad-Core", "")

    # 4. Rimuove spazi bianchi extra all'inizio e alla fine
    name = name.strip()

    return name

def process_files(file_list):
    for file_name in file_list:
        if not os.path.exists(file_name):
            print(f"File non trovato: {file_name}")
            continue
            
        print(f"Elaborazione di {file_name}...")
        
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Contatori per statistiche
            modified_count = 0
            
            # Itera su ogni elemento e normalizza il nome
            for entry in data:
                if 'name' in entry:
                    original = entry['name']
                    normalized = normalize_hardware_name(original)
                    
                    # Aggiorna il nome nel dizionario
                    entry['name_normalized'] = normalized # Salva in un nuovo campo (opzionale)
                    # entry['name'] = normalized          # Decommenta per sovrascrivere
                    
                    if original != normalized:
                        modified_count += 1
                        # Stampa un esempio delle prime modifiche
                        if modified_count <= 3:
                            print(f"  Cambio: '{original}' -> '{normalized}'")

            # Salva il nuovo file con prefisso 'normalized_'
            output_name = f"normalized_{file_name}"
            with open(output_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            
            print(f"Fatto. {modified_count} nomi normalizzati. Salvato in: {output_name}\n")

        except Exception as e:
            print(f"Errore durante l'elaborazione di {file_name}: {e}")

# Esecuzione dello script
if __name__ == "__main__":
    # Assicurati che i file siano nella stessa cartella dello script o specifica il percorso completo
    process_files(files_to_process)