import json
import os
import sys
from typing import Dict, List, Optional

def analyze_replays(replay_dir: str, cache_file: str, model_id: str, output_dir: Optional[str] = None) -> List[Dict]:
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    cache = {}
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cache = json.load(f)
            print(f"Loaded {len(cache)} cached analyses.")
        except Exception as e:
            print(f"Could not load cache: {e}. Starting fresh.")

    json_files = glob.glob(os.path.join(replay_dir, "*.json"))
    print(f"Found {len(json_files)} replay files in {replay_dir}.")

    results = []
    
    # Sort files to be deterministic
    json_files.sort()

    # Filter out the cache file itself if it's in the same dir and has .json extension
    json_files = [f for f in json_files if os.path.abspath(f) != os.path.abspath(cache_file)]


def analyze_replays(replay_dir: str, cache_file: str, model_id: str, output_dir: Optional[str] = None, max_workers: int = 20, max_retries: int = 10) -> List[Dict]:
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    cache = {}
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cache = json.load(f)
            print(f"Loaded {len(cache)} cached analyses.")
        except Exception as e:
            print(f"Could not load cache: {e}. Starting fresh.")

    json_files = glob.glob(os.path.join(replay_dir, "*.json"))
    print(f"Found {len(json_files)} replay files in {replay_dir}.")
    
    # Sort files to be deterministic
    json_files.sort()

    # Filter out the cache file itself
    json_files = [f for f in json_files if os.path.abspath(f) != os.path.abspath(cache_file)]
    
    results = []
    new_entries_count = 0
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    print(f"Starting analysis with {max_workers} workers...")
    
    
    executor = ThreadPoolExecutor(max_workers=max_workers)
    try:
        # Submit all tasks
        future_to_file = {
            executor.submit(analyze_single_game, f, cache, model_id, output_dir, max_retries): f 
            for f in json_files
        }
        
        with tqdm(total=len(json_files), desc="Analyzing Games") as pbar:
            for future in as_completed(future_to_file):
                json_file = future_to_file[future]
                try:
                    result, file_hash, is_new = future.result()
                    if result:
                        results.append(result)
                        if is_new and file_hash:
                            cache[file_hash] = result
                            new_entries_count += 1
                except Exception as e:
                    print(f"Exception analyzing {json_file}: {e}")
                finally:
                    pbar.update(1)
                
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user. Shutting down workers...")
        executor.shutdown(wait=False, cancel_futures=True)
        # Still try to save whatever we have cached so far
        if new_entries_count > 0:
             print(f"Saving {new_entries_count} new entries before exit...")
             try:
                with open(cache_file, 'w') as f:
                    json.dump(cache, f, indent=2)
             except: pass
        sys.stdout.flush()
        # Force exit to kill non-daemon threads from file executor
        os._exit(1)
    finally:
        # multiple calls to shutdown are safe
        executor.shutdown(wait=False, cancel_futures=True)

    # Save updated cache at the end if we added anything
    if new_entries_count > 0:
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
            print(f"Updated cache with {new_entries_count} new entries.")
        except Exception as e:
            print(f"Warning: Failed to write cache: {e}")
    else:
        print("No new analyses to cache.")

    return results

