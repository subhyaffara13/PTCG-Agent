import os
import subprocess

def process_single_episode_direct(replay_file, bucket_base, config_path, tts_provider, prompt_path, cache_path, enable_llm, keep_temp=False, position=0):
    episode_id = os.path.splitext(os.path.basename(replay_file))[0]
    temp_out_dir = f"temp_audio_output/{episode_id}"
    
    # Ensure clean state
    if os.path.exists(temp_out_dir):
        shutil.rmtree(temp_out_dir)
    os.makedirs(temp_out_dir, exist_ok=True)
    
    success = False

    try:
        # 1. Generate Audio (Direct Python Call)
        # Pass TQDM kwargs for positioning
        tqdm_kwargs = {
            "position": position + 1, # Offset by 1 to leave room for main bar? Or main bar at 0?
             # Actually, if main bar is at 0, we use position N+1.
            "leave": False,
            "desc": f"Gen {episode_id}",
            "ncols": 80, # Limit width to avoid wrapping
            "mininterval": 0.5
        }
        
        # We need to capture stdout/stderr to separate logs from bars?
        # But add_audio prints to stdout/stderr.
        # Ideally we silence add_audio logging or redirect it.
        # But user wants bars. Bars print to stderr usually.
        
        add_audio.process_replay_file(
            input_path=replay_file,
            output_dir=temp_out_dir,
            config_path=config_path,
            tts_provider=tts_provider,
            prompt_path=prompt_path,
            cache_path=cache_path,
            disable_llm=not enable_llm,
            tqdm_kwargs=tqdm_kwargs
        )

        # Check if output directory has content
        # add_audio creates a subdirectory "audio" by default (standard.yaml)
        # We should check inside that validation.
        audio_subdir = os.path.join(temp_out_dir, "audio")
        
        if not os.path.isdir(audio_subdir):
             return False, f"No 'audio' subdirectory generated for {episode_id}"

        files = os.listdir(audio_subdir)
        if not files:
             return False, f"No audio files generated for {episode_id} (Audio dir empty)"
        
        wav_files = [f for f in files if f.endswith(".wav")]
        if len(wav_files) < 5:
             return False, f"Suspiciously low audio file count ({len(wav_files)}) for {episode_id}. Check logs."

        # 2. Upload to GCS
        target_path = f"{bucket_base}/{episode_id}"
        # Use gcloud storage rsync for robust directory synchronization
        upload_cmd = f"gcloud storage rsync '{temp_out_dir}' '{target_path}' --recursive"
        
        # We capture output to avoid spamming the console heavily, 
        # but maybe user wants to see upload progress too? 
        # For now, let's keep capture_output=True for upload to keep bars clean.
        upload_result = subprocess.run(
            upload_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if upload_result.returncode != 0:
             return False, f"Upload failed for {episode_id}: {upload_result.stderr}"

        success = True

    except Exception as e:
        return False, f"Exception in {episode_id}: {str(e)}"
    finally:
        # Cleanup ONLY if successful and not keeping temp
        if success and not keep_temp and os.path.exists(temp_out_dir):
            shutil.rmtree(temp_out_dir)
            
    return True, episode_id

