
def analyze_single_game(json_file: str, cache: Dict, model_id: str, output_dir: Optional[str], max_retries: int = 10) -> Optional[Dict]:
    """
    Analyzes a single game replay.
    Returns the analysis dict (either from cache or fresh) or None if failed.
    """
    try:
        file_hash = get_file_hash(json_file)
        
        # Check in-memory cache first (though typical usage expects cache populated initially)
        if file_hash in cache:
             # print(f"Skipping {os.path.basename(json_file)} (Cached)")
             cached_result = cache[file_hash]
             cached_result["_filename"] = os.path.basename(json_file)
             return cached_result, file_hash, False
        
        # Check if summary json exists in output_dir
        if output_dir:
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            summary_path = os.path.join(output_dir, f"{base_name}_summary.json")
            if os.path.exists(summary_path):
                try:
                    with open(summary_path, 'r') as f:
                        existing_analysis = json.load(f)
                    # We assume if the summary exists, it's valid. 
                    # We might want to backfill _filename if missing
                    existing_analysis["_filename"] = os.path.basename(json_file)
                    # Update cache with this existing result so next run is faster
                    # Note: We won't have the compute hash if we just load json, 
                    # but we computed file_hash above.
                    return existing_analysis, file_hash, True 
                except Exception as e:
                    print(f"Warning: Failed to load existing summary {summary_path}: {e}")

        # If not in cache and not on disk, proceed with analysis

        print(f"Processing {os.path.basename(json_file)}...")
        transcript, turn_count = summarize_game.extract_game_transcript(json_file)

        if "Error:" in transcript[:50] and len(transcript) < 200:
                print(f"Skipping {json_file}: {transcript}")
                return None, file_hash, False

        if len(transcript) < 100:
            print(f"Skipping {json_file}: Transcript too short.")
            return None, file_hash, False
            
        analysis = summarize_game.summarize_with_gemini(transcript, model_id=model_id, max_retries=max_retries)
        if analysis:
            analysis.total_turns = turn_count
            analysis_dict = analysis.model_dump()
            analysis_dict["_filename"] = os.path.basename(json_file)
            
            if output_dir:
                base_name = os.path.splitext(os.path.basename(json_file))[0]
                summary_path = os.path.join(output_dir, f"{base_name}_summary.json")
                with open(summary_path, 'w') as f:
                    json.dump(analysis_dict, f, indent=2)
                
                transcript_path = os.path.join(output_dir, f"{base_name}_transcript.txt")
                with open(transcript_path, 'w') as f:
                    f.write(transcript)
            
            return analysis_dict, file_hash, True
        else:
                print(f"Failed to analyze {json_file} (LLM returned None)")
                return None, file_hash, False

    except Exception as e:
        print(f"Error processing {json_file}: {e}")
        return None, None, False

