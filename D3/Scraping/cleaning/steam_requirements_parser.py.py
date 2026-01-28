import json
import re
import pandas as pd
from pathlib import Path
# 1. Load Data
# input_filename = '/home/andreea/GameMatcher/D3/Scraping/deta/steam_top_100.json' 
input_filename = Path(r"C:\Users\tomma\Desktop\Clone Repository Actionable Knowledge\GameMatcher\D3\Scraping\row data\steam_top_100.json")
# Ensure the file is in the same folder or provide the full path
with open(input_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# --- PARSING FUNCTIONS ---

def clean_hardware_string(text):
    if not isinstance(text, str) or text == "N/A":
        return ""
    
    # Remove trademarks and newlines
    text = text.replace("®", "").replace("™", "").replace("\n", " ")
    
    # Remove noise words that confuse the parser
    noise = [" or equivalent", " or better", "compatible with", "support for", 
             "graphics card", "video card", "processor", "hardware cpu threads"]
    for word in noise:
        text = text.replace(word, "")
    
    # Remove extra spaces
    return re.sub(r'\s+', ' ', text).strip()

def extract_models(text):
    clean_text = clean_hardware_string(text)
    if not clean_text:
        return []

    # Heuristics to identify generic descriptions (DIFFICULT CASES)
    if "must be" in clean_text.lower() or "level video" in clean_text.lower():
        return [] # Return empty to force the game into the "Difficult" file

    # Regex separators: / or | or "or" or comma
    split_pattern = r'\s*(?:/|\||;|\s+or\s+|\s+OR\s+|,\s*|\s+//\s+)\s*'
    parts = re.split(split_pattern, clean_text, flags=re.IGNORECASE)
    
    candidates = []
    for part in parts:
        part = part.strip()
        
        # Filter: must be longer than 2 chars and not start with DirectX
        if len(part) > 2 and not part.lower().startswith("directx"):
            
            # VRAM/Clock cleanup
            part_clean = re.sub(r'\s*\(.*?\)|(\d+\s*GB\+?(\s*VRAM)?)$|(\d+(\.\d+)?\s*GHz)$', '', part, flags=re.IGNORECASE).strip()
            
            # Final check
            if len(part_clean) < 30 and part_clean:
                candidates.append(part_clean)
            
    return candidates

# --- LOGIC APPLICATION ---

# 1. Extract lists
df['CPU_List'] = df['CPU'].apply(extract_models)
df['GPU_List'] = df['GPU'].apply(extract_models)

# 2. Classification Logic (Easy vs Difficult)
def classify_row(row):
    if not row['CPU_List'] or not row['GPU_List']:
        return 'Difficult'
    return 'Easy'

df['Complexity'] = df.apply(classify_row, axis=1)

# --- DATASET CREATION ---

# EASY Dataset (Clean)
df_clean = df[df['Complexity'] == 'Easy'].copy()

# Expand GPU columns
gpu_expanded = df_clean['GPU_List'].apply(pd.Series).add_prefix('GPU_')
cpu_expanded = df_clean['CPU_List'].apply(pd.Series).add_prefix('CPU_')

# Merge everything
df_clean_final = pd.concat([df_clean.drop(['CPU', 'GPU', 'CPU_List', 'GPU_List', 'Complexity'], axis=1), 
                           gpu_expanded, cpu_expanded], axis=1)

# DIFFICULT Dataset (Dirty)
df_dirty = df[df['Complexity'] == 'Difficult'][['NAME', 'CPU', 'GPU', 'PRICE']].copy()

# --- SAVING (FIXED for NULLs) ---
import json

def save_clean_json(dataframe, filename):
    dataframe = dataframe.astype(object).where(pd.notnull(dataframe), None)

    # Convert DataFrame to a list of Python dictionaries
    data = dataframe.to_dict(orient='records')
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Save the two files using the new function
save_clean_json(df_clean_final, 'steam_parsed_CLEAN.json')
save_clean_json(df_dirty, 'steam_parsed_COMPLEX.json')

# Output for verification
print(f"Total games analyzed: {len(df)}")
print(f"Saved 'Clean' games: {len(df_clean_final)}")
print(f"Saved 'To Review' games: {len(df_dirty)}")
print("Done! Files now use 'null' instead of NaN.")

# Example output check
if not df_clean_final.empty:
    cols_to_show = ['NAME'] + [col for col in df_clean_final.columns if 'GPU_' in col][:2]
    # Note: printing here might still show NaN because pandas prints that way, 
    # but check the actual .json file for 'null'
    print(df_clean_final[cols_to_show].head(3).to_string())
else:
    print("No clean games found to display.")