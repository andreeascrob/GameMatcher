import json
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# AUTOMATIC CONFIGURATION (DO NOT TOUCH)
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()

DIR_CLEANING = SCRIPT_DIR
DIR_RAW = os.path.join(os.path.dirname(SCRIPT_DIR), "row data")

print(f"Script Directory (Clean): {DIR_CLEANING}")
print(f"Raw Data Directory:       {DIR_RAW}")

files_map = {
    "steam_raw":    os.path.join(DIR_RAW, "steam_top_100.json"),
    "cpu_raw":      os.path.join(DIR_RAW, "cpu_data.json"),
    "gpu_raw":      os.path.join(DIR_RAW, "gpu_data.json"),
    
    "steam_clean":  os.path.join(DIR_CLEANING, "steam_parsed_CLEAN.json"),
    "cpu_filtered": os.path.join(DIR_CLEANING, "cpu_filtered.json"),
    "gpu_filtered": os.path.join(DIR_CLEANING, "gpu_filtered.json")
}

#DATA LOADING
data = {}
print("\n--- STARTING LOAD ---")

all_files_found = True

for key, path in files_map.items():
    if not os.path.exists(path):
        print(f"[ERROR] File NOT found: {path}")
        data[key] = []
        all_files_found = False
    else:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data[key] = json.load(f)

        except Exception as e:
            print(f"[READ ERROR] {path}: {e}")
            data[key] = []

if not all_files_found:
    print("\n[WARNING] Some files were not found. Statistics might be incorrect.")
    print("Check that the 'row data' folder is at the same level as 'cleaning'.")

if not data["steam_raw"] and not data["steam_clean"]:
    print("\n[CRITICAL STOP] No Steam data found. Script terminated.")
    sys.exit()

# STATISTICS CALCULATION
len_s_raw = len(data["steam_raw"])
len_s_clean = len(data["steam_clean"])
len_c_raw = len(data["cpu_raw"])
len_c_filt = len(data["cpu_filtered"])
len_g_raw = len(data["gpu_raw"])
len_g_filt = len(data["gpu_filtered"])

# Percentages
perc_cpu = round((1 - len_c_filt/len_c_raw)*100, 2) if len_c_raw > 0 else 0
perc_gpu = round((1 - len_g_filt/len_g_raw)*100, 2) if len_g_raw > 0 else 0

print("\n" + "="*40)
print(" FINAL REPORT")
print("="*40)
print(f"1. STEAM GAMES")
print(f"   - Total Scraped:    {len_s_raw}")
print(f"   - Usable (Clean):   {len_s_clean}")
print(f"   - Discarded:        {len_s_raw - len_s_clean}")

print(f"\n2. HARDWARE (Knowledge Graph Optimization)")
print(f"   - CPU: From {len_c_raw} -> to {len_c_filt} (Reduction: {perc_cpu}%)")
print(f"   - GPU: From {len_g_raw} -> to {len_g_filt} (Reduction: {perc_gpu}%)")
print("="*40 + "\n")


plt.style.use('ggplot')

# Chart 1: Steam
try:
    plt.figure(figsize=(8, 6))
    labels = ['Usable Games', 'Discarded']
    vals = [len_s_clean, len_s_raw - len_s_clean]
    plt.bar(labels, vals, color=['#2ecc71', '#e74c3c'], edgecolor='black', width=0.5)
    plt.title('Steam Data Parsing Efficiency')
    plt.ylabel('Games Count')
    
    for i, v in enumerate(vals):
        plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')

    
    path_img1 = os.path.join(DIR_CLEANING, "stat_steam.png")
    plt.tight_layout()
    plt.savefig(path_img1)
    print(f"Chart generated: {path_img1}")
    plt.close() 
except Exception as e:
    print(f"Error generating Chart 1: {e}")

# Chart 2: Hardware 
try:
    plt.figure(figsize=(10, 6))
    labels_hw = ['CPU', 'GPU']
    raw_v = [len_c_raw, len_g_raw]
    filt_v = [len_c_filt, len_g_filt]
    x = np.arange(len(labels_hw))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, raw_v, width, label='Full Benchmark DB', color='gray')
    rects2 = ax.bar(x + width/2, filt_v, width, label='Optimized (Graph)', color='purple')

    ax.set_title('Knowledge Graph Optimization')
    ax.set_xticks(x)
    ax.set_xticklabels(labels_hw)
    ax.legend()
    ax.set_ylabel('Count')

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.annotate(f'{h}', xy=(rect.get_x() + rect.get_width()/2, h),
                        xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)

    path_img2 = os.path.join(DIR_CLEANING, "stat_hardware.png")
    plt.tight_layout()
    plt.savefig(path_img2)
    print(f"Chart generated: {path_img2}")
    plt.close()
except Exception as e:
    print(f"Error generating Chart 2: {e}")

