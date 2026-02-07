import json
import re
from difflib import SequenceMatcher
from copy import deepcopy
from pathlib import Path

# --- UNIVERSAL PATH SETUP ---
# Path(__file__).parent points to the 'cleaning' folder where this script lives
BASE_DIR = Path(__file__).parent 

# Define and create the output directory
FILTERED_DIR = BASE_DIR / "filtered data"
FILTERED_DIR.mkdir(parents=True, exist_ok=True)

# Inputs: Going up one level to 'Scraping', then into 'cleaning' or 'raw data'
STEAM_FILE = BASE_DIR / "steam_parsed_CLEAN.json"
CPU_DATA_FILE = BASE_DIR.parent / "raw data" / "cpu_data.json"
GPU_DATA_FILE = BASE_DIR.parent / "raw data" / "gpu_data.json"

# Outputs: Pointing inside the new 'filtered data' folder
OUT_CPU_FILE = FILTERED_DIR / "cpu_filtered.json"
OUT_GPU_FILE = FILTERED_DIR / "gpu_filtered.json"

# --- STRING NORMALIZATION ---
def canonical_name(text):
    """Standardizes names by removing noise to make fuzzy matching more accurate."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"@.*?ghz", "", text)
    text = re.sub(r"®|™", "", text)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return re.sub(r"\s+", " ", text).strip()

# --- SIMILARITY LOGIC ---
def similarity(a, b):
    """Calculates a matching ratio between two strings (0.0 to 1.0)."""
    return SequenceMatcher(None, a, b).ratio()

# --- DATA EXTRACTION ---
def extract_components(steam_data, prefix):
    """Scans Steam data for unique hardware entries based on prefix (CPU_ or GPU_)."""
    canonical = {}
    for game in steam_data:
        for k, v in game.items():
            if k.startswith(prefix) and v:
                v = v.strip()
                if v.lower() in {"similar", "equivalent"}:
                    continue
                key = canonical_name(v)
                canonical[key] = v  
    return canonical

# --- MATCHING ENGINE ---
def best_match(canon_steam, full_data):
    """Finds the most likely hardware match from the reference database."""
    candidates = []
    for item in full_data:
        name = item.get("name")
        if not name: continue

        canon_name = canonical_name(name)
        if canon_steam in canon_name or canon_name in canon_steam:
            sim = similarity(canon_steam, canon_name)
            candidates.append((sim, item))

    if not candidates:
        return None

    max_sim = max(c[0] for c in candidates)
    best = [c[1] for c in candidates if c[0] == max_sim]
    return min(best, key=lambda x: x.get("mark", float("inf")))

# --- DATA RECONSTRUCTION ---
def build_filtered(steam_map, full_data):
    """Builds a new list with technical data for every successful match."""
    filtered = {}
    for canon_steam, steam_name in steam_map.items():
        match = best_match(canon_steam, full_data)
        if not match:
            continue
        unified = deepcopy(match)
        unified["name"] = steam_name  
        filtered[canon_steam] = unified  
    return list(filtered.values())

# --- EXECUTION FLOW ---
def main():
    """Main execution flow with explicit path handling."""
    print(f"Reading from: {BASE_DIR.parent}")
    
    # Check if files exist before opening
    for p in [STEAM_FILE, CPU_DATA_FILE, GPU_DATA_FILE]:
        if not p.exists():
            print(f"❌ Error: File not found at {p}")
            return

    # Load all datasets
    with open(STEAM_FILE, encoding="utf-8") as f:
        steam_data = json.load(f)
    with open(CPU_DATA_FILE, encoding="utf-8") as f:
        cpu_data = json.load(f)
    with open(GPU_DATA_FILE, encoding="utf-8") as f:
        gpu_data = json.load(f)

    # Process
    steam_cpus = extract_components(steam_data, "CPU_")
    steam_gpus = extract_components(steam_data, "GPU_")
    cpu_filtered = build_filtered(steam_cpus, cpu_data)
    gpu_filtered = build_filtered(steam_gpus, gpu_data)

    # Save
    with open(OUT_CPU_FILE, "w", encoding="utf-8") as f:
        json.dump(cpu_filtered, f, indent=2, ensure_ascii=False)
    with open(OUT_GPU_FILE, "w", encoding="utf-8") as f:
        json.dump(gpu_filtered, f, indent=2, ensure_ascii=False)

    print(f"✔ Files saved to: {BASE_DIR}")
    print(f"✔ Final CPU entries: {len(cpu_filtered)}")
    print(f"✔ Final GPU entries: {len(gpu_filtered)}")

if __name__ == "__main__":
    main()