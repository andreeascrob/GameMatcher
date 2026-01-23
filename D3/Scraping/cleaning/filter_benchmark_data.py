import json
import pandas as pd
import difflib

# --- FILE CONFIGURATION ---
steam_file = '/home/andreea/GameMatcher/D3/Scraping/pulizia/steam_parsed_CLEAN.json'      # Your cleaned Steam file
gpu_bench_file = '/home/andreea/GameMatcher/D3/Scraping/deta/gpu_data.json'            # The huge GPU file
cpu_bench_file = '/home/andreea/GameMatcher/D3/Scraping/deta/cpu_data.json'            # The huge CPU file

output_gpu = 'filtered_gpu_data.json'       # Desired output
output_cpu = 'filtered_cpu_data.json'       # Desired output
mapping_log = 'hardware_mapping_log.txt'    # File to check matches

# --- FUNCTIONS ---

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found -> {filepath}")
        return []

def extract_unique_hardware(steam_data, type_prefix, max_index):
    """
    Extracts a unique set of hardware names from columns (e.g., GPU_0 ... GPU_7)
    """
    unique_hardware = set()
    df = pd.DataFrame(steam_data)
    
    for i in range(max_index + 1):
        col_name = f"{type_prefix}_{i}"
        if col_name in df.columns:
            # Takes non-null values and adds them to the set
            items = df[col_name].dropna().unique()
            for item in items:
                if item and str(item).strip():
                    unique_hardware.add(str(item).strip())
    
    return list(unique_hardware)

def find_best_match_and_filter(target_names, benchmark_data, hardware_type):
    """
    Searches for Steam names inside the benchmark data using fuzzy matching.
    Returns:
    1. The list of filtered benchmark data.
    2. A text log of what was mapped.
    """
    filtered_data = []
    seen_benchmark_names = set() # To avoid duplicates in the final file
    mapping_info = []

    # Create a dictionary {benchmark_name: benchmark_object} for quick access
    bench_dict = {item['name']: item for item in benchmark_data if 'name' in item}
    all_bench_names = list(bench_dict.keys())

    print(f"\n--- Starting {hardware_type} Matching ---")
    print(f"Searching for {len(target_names)} unique Steam models in {len(all_bench_names)} benchmarks...")

    found_count = 0

    for target in target_names:
        # 1. Exact Match Attempt
        match = None
        
        # 2. Fuzzy Match Attempt (if not exact)
        # cutoff=0.5 means they must be 50% similar
        # n=1 takes only the best match
        matches = difflib.get_close_matches(target, all_bench_names, n=1, cutoff=0.5)
        
        if matches:
            best_match_name = matches[0]
            
            # Retrieve data
            bench_entry = bench_dict[best_match_name]
            
            # Log the result
            mapping_info.append(f"[STEAM] '{target}'  -->  [BENCHMARK] '{best_match_name}' (Mark: {bench_entry.get('mark')})")
            
            # Add to final list if we haven't taken it already
            if best_match_name not in seen_benchmark_names:
                filtered_data.append(bench_entry)
                seen_benchmark_names.add(best_match_name)
            
            found_count += 1
        else:
            mapping_info.append(f"[MISSING] '{target}' not found in benchmark.")

    print(f"Found {found_count} out of {len(target_names)} requested hardware items.")
    return filtered_data, mapping_info

# --- EXECUTION ---

# 1. Load Data
print("Loading files...")
steam_data = load_json(steam_file)
gpu_bench = load_json(gpu_bench_file)
cpu_bench = load_json(cpu_bench_file)

if steam_data and gpu_bench and cpu_bench:
    
    # 2. Extract unique names from Steam
    # For GPUs we look from 0 to 7
    steam_gpus = extract_unique_hardware(steam_data, "GPU", 7)
    # For CPUs we look from 0 to 3
    steam_cpus = extract_unique_hardware(steam_data, "CPU", 3)

    # 3. Filtering and Matching
    filtered_gpus, gpu_log = find_best_match_and_filter(steam_gpus, gpu_bench, "GPU")
    filtered_cpus, cpu_log = find_best_match_and_filter(steam_cpus, cpu_bench, "CPU")

    # 4. Save Filtered JSONs
    with open(output_gpu, 'w', encoding='utf-8') as f:
        json.dump(filtered_gpus, f, indent=4)
    
    with open(output_cpu, 'w', encoding='utf-8') as f:
        json.dump(filtered_cpus, f, indent=4)

    # 5. Save Log (useful for debug)
    with open(mapping_log, 'w', encoding='utf-8') as f:
        f.write("--- GPU MAPPING ---\n")
        f.write("\n".join(gpu_log))
        f.write("\n\n--- CPU MAPPING ---\n")
        f.write("\n".join(cpu_log))

    print(f"\nDone! Files saved:")
    print(f"1. {output_gpu} (Contains {len(filtered_gpus)} GPUs)")
    print(f"2. {output_cpu} (Contains {len(filtered_cpus)} CPUs)")
    print(f"3. {mapping_log} (Check here if matches are correct)")

else:
    print("Cannot proceed due to missing files.")