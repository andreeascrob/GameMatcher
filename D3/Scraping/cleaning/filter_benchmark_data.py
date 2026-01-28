import json
import re
from difflib import SequenceMatcher
from copy import deepcopy



STEAM_FILE = "../GameMatcher/D3/Scraping/cleaning/steam_parsed_CLEAN.json"
CPU_DATA_FILE = "../GameMatcher/D3/Scraping/row data/cpu_data.json"
GPU_DATA_FILE = "../GameMatcher/D3/Scraping/row data/gpu_data.json"

OUT_CPU_FILE = "cpu_filtered.json"
OUT_GPU_FILE = "gpu_filtered.json"


def canonical_name(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"@.*?ghz", "", text)
    text = re.sub(r"®|™", "", text)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def extract_components(steam_data, prefix):
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


def best_match(canon_steam, full_data):
    candidates = []

    for item in full_data:
        name = item.get("name")
        if not name:
            continue

        canon_name = canonical_name(name)

        if canon_steam in canon_name or canon_name in canon_steam:
            sim = similarity(canon_steam, canon_name)
            candidates.append((sim, item))

    if not candidates:
        return None

    max_sim = max(c[0] for c in candidates)
    best = [c[1] for c in candidates if c[0] == max_sim]

    return min(best, key=lambda x: x.get("mark", float("inf")))


def build_filtered(steam_map, full_data):
    filtered = {}

    for canon_steam, steam_name in steam_map.items():
        match = best_match(canon_steam, full_data)
        if not match:
            continue

        unified = deepcopy(match)
        unified["name"] = steam_name  

        filtered[canon_steam] = unified  

    return list(filtered.values())


def main():
    with open(STEAM_FILE, encoding="utf-8") as f:
        steam_data = json.load(f)

    with open(CPU_DATA_FILE, encoding="utf-8") as f:
        cpu_data = json.load(f)

    with open(GPU_DATA_FILE, encoding="utf-8") as f:
        gpu_data = json.load(f)

    steam_cpus = extract_components(steam_data, "CPU_")
    steam_gpus = extract_components(steam_data, "GPU_")

    cpu_filtered = build_filtered(steam_cpus, cpu_data)
    gpu_filtered = build_filtered(steam_gpus, gpu_data)

    with open(OUT_CPU_FILE, "w", encoding="utf-8") as f:
        json.dump(cpu_filtered, f, indent=2, ensure_ascii=False)

    with open(OUT_GPU_FILE, "w", encoding="utf-8") as f:
        json.dump(gpu_filtered, f, indent=2, ensure_ascii=False)

    print(f"✔ CPU uniche finali: {len(cpu_filtered)}")
    print(f"✔ GPU uniche finali: {len(gpu_filtered)}")


if __name__ == "__main__":
    main()
