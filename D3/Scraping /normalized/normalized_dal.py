import json
import re
import os

FILES_TO_PROCESS = [
    "cpu_data.json",
    "gpu_data.json",
    "hardware_data.json"
]

# =========================
# CPU NORMALIZATION
# =========================
def normalize_cpu_name(name):
    if not isinstance(name, str):
        return None

    name = name.upper()

    # Intel Core i3/i5/i7/i9
    intel = re.search(r'INTEL.*CORE\s+(I[3579])[-\s]?(\d{4,5})', name)
    if intel:
        return f"Intel Core {intel.group(1)} {intel.group(2)}"

    # AMD Ryzen 3/5/7/9
    amd = re.search(r'AMD.*RYZEN\s+([3579])\s+(\d{4,5})', name)
    if amd:
        return f"AMD Ryzen {amd.group(1)} {amd.group(2)}"

    return None


# =========================
# GPU NORMALIZATION
# =========================
def normalize_gpu_name(name):
    if not isinstance(name, str):
        return None

    name = name.upper()

    # NVIDIA RTX
    rtx = re.search(r'RTX\s*(\d{4})', name)
    if rtx:
        return f"NVIDIA RTX {rtx.group(1)}"

    # NVIDIA GTX
    gtx = re.search(r'GTX\s*(\d{3,4})', name)
    if gtx:
        return f"NVIDIA GTX {gtx.group(1)}"

    # AMD RX
    rx = re.search(r'RX\s*(\d{3,4})', name)
    if rx:
        return f"AMD RX {rx.group(1)}"

    # Intel Arc
    arc = re.search(r'ARC\s*A(\d{3})', name)
    if arc:
        return f"Intel Arc A{arc.group(1)}"

    return None


# =========================
# FILE PROCESSING
# =========================
def process_files(files):
    for file_name in files:
        if not os.path.exists(file_name):
            print(f"❌ File non trovato: {file_name}")
            continue

        print(f"\n📂 Elaborazione: {file_name}")

        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)

        cleaned_data = []
        removed = 0

        for entry in data:
            name = entry.get("name", "")

            if "cpu" in file_name.lower():
                normalized = normalize_cpu_name(name)

            elif "gpu" in file_name.lower():
                normalized = normalize_gpu_name(name)

            else:
                # hardware_data.json → prova prima CPU poi GPU
                normalized = normalize_cpu_name(name)
                if not normalized:
                    normalized = normalize_gpu_name(name)

            if normalized:
                entry["name_normalized"] = normalized
                cleaned_data.append(entry)
            else:
                removed += 1

        output_file = f"normalized_{file_name}"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4)

        print(f"✅ Tenuti: {len(cleaned_data)} | 🗑 Rimossi: {removed}")
        print(f"💾 Salvato in: {output_file}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    process_files(FILES_TO_PROCESS)
