import json
import re
import pandas as pd

# 1. Caricamento Dati
input_filename = '/home/andreea/GameMatcher/D3/Scraping/deta/steam_top_100.json' 
# Assicurati che il file sia nella stessa cartella o metti il percorso completo
with open(input_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# --- FUNZIONI DI PARSING ---

def clean_hardware_string(text):
    if not isinstance(text, str) or text == "N/A":
        return ""
    
    # Rimuove trademark e newlines
    text = text.replace("®", "").replace("™", "").replace("\n", " ")
    
    # Rimuove parole inutili che confondono il parser
    noise = [" or equivalent", " or better", "compatible with", "support for", 
             "graphics card", "video card", "processor", "hardware cpu threads"]
    for word in noise:
        text = text.replace(word, "")
    
    # Rimuove spazi extra
    return re.sub(r'\s+', ' ', text).strip()

def extract_models(text):
    clean_text = clean_hardware_string(text)
    if not clean_text:
        return []

    # Euristiche per identificare descrizioni generiche (CASI DIFFICILI)
    # Se la stringa contiene parole troppo generiche e nessun numero/modello chiaro
    if "must be" in clean_text.lower() or "level video" in clean_text.lower():
        return [] # Ritorna vuoto per forzare il gioco nel file "Difficili"

    # Regex separatori: / o | o "or" o virgola
    split_pattern = r'\s*(?:/|\||;|\s+or\s+|\s+OR\s+|,\s*|\s+//\s+)\s*'
    parts = re.split(split_pattern, clean_text, flags=re.IGNORECASE)
    
    candidates = []
    for part in parts:
        part = part.strip()
        
        # Filtro: deve essere più lungo di 2 char e non iniziare con DirectX
        if len(part) > 2 and not part.lower().startswith("directx"):
            
            # Pulizia VRAM/Clock: toglie (6GB), 4GB, 3.5GHz ecc alla fine della stringa
            # Esempio: "GTX 1060 (6GB)" -> "GTX 1060"
            part_clean = re.sub(r'\s*\(.*?\)|(\d+\s*GB\+?(\s*VRAM)?)$|(\d+(\.\d+)?\s*GHz)$', '', part, flags=re.IGNORECASE).strip()
            
            # Controllo finale: se la stringa pulita è ancora troppo lunga (es. > 30 char)
            # probabilmente è una frase descrittiva, non un modello.
            if len(part_clean) < 30 and part_clean:
                candidates.append(part_clean)
            
    return candidates

# --- APPLICAZIONE LOGICA ---

# 1. Estraiamo le liste
df['CPU_List'] = df['CPU'].apply(extract_models)
df['GPU_List'] = df['GPU'].apply(extract_models)

# 2. Logica di Classificazione (Facile vs Difficile)
def classify_row(row):
    # Se CPU o GPU sono vuote (o N/A), o se le liste estratte sono vuote -> Difficile
    if not row['CPU_List'] or not row['GPU_List']:
        return 'Difficile'
    return 'Facile'

df['Complexity'] = df.apply(classify_row, axis=1)

# --- CREAZIONE DEI DUE DATASET ---

# Dataset FACILE (Clean)
df_clean = df[df['Complexity'] == 'Facile'].copy()

# Espandiamo le colonne GPU (gpu1, gpu2, gpu3...)
gpu_expanded = df_clean['GPU_List'].apply(pd.Series).add_prefix('GPU_')
cpu_expanded = df_clean['CPU_List'].apply(pd.Series).add_prefix('CPU_')

# Uniamo tutto e rimuoviamo le colonne vecchie
df_clean_final = pd.concat([df_clean.drop(['CPU', 'GPU', 'CPU_List', 'GPU_List', 'Complexity'], axis=1), 
                           gpu_expanded, cpu_expanded], axis=1)

# Dataset DIFFICILE (Dirty)
# Qui manteniamo le colonne originali così puoi leggerle e capire come fixarle
df_dirty = df[df['Complexity'] == 'Difficile'][['NAME', 'CPU', 'GPU', 'PRICE']].copy()

# --- SALVATAGGIO ---

df_clean_final.to_json('steam_parsed_CLEAN.json', orient='records', indent=4)
df_dirty.to_json('steam_parsed_COMPLEX.json', orient='records', indent=4)

# Output per verifica
print(f"Totale giochi analizzati: {len(df)}")
print(f"Giochi 'Puliti' salvati: {len(df_clean_final)}")
print(f"Giochi 'Da revisionare' salvati: {len(df_dirty)}")

# Mostra un esempio di come vengono separate le colonne
print("\n--- Esempio Output Pulito (Prime righe) ---")
cols_to_show = ['NAME', 'GPU_0', 'GPU_1'] 
# Nota: Pandas usa 0, 1... se vuoi 1, 2 devi rinominare, ma la logica è questa
print(df_clean_final[cols_to_show].head(3).to_string())