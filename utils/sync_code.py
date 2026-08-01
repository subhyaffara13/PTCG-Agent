import os
import logging
import subprocess
from utils._run_git import _run_git
from utils.get_local_version import get_local_version

def sync_code(master_version) -> bool:
    local_version = get_local_version()
    if not local_version or not master_version:
        logging.info("Version info unavailable. Skipping code sync.")
        return False

    if local_version != master_version:
        logging.info(f"Version mismatch. Local: {local_version}, Master: {master_version}. Pulling...")
        try:
            _run_git(['git', 'fetch', '--all'], check=True, capture_output=True, text=True)
            files_to_clean = [
                "models/ppo_actor_critic.pt",
                "cb_agents/deck_new.csv",
                "skills/learned_dos.json",
                "skills/predictor_feedback.json",
                "skills/predictor_weights.json"
            ]
            for f in files_to_clean:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception as clean_err:
                        logging.warning(f"Could not remove {f} before reset: {clean_err}")
            
            try:
                _run_git(['git', 'reset', '--hard', master_version], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError:
                _run_git(['git', 'reset', '--hard', 'origin/main'], check=True)
                
            new_local_version = get_local_version()
            if new_local_version:
                logging.info(f"Code synchronized successfully from {local_version} to {new_local_version}.")
                return True
            return False
        except subprocess.CalledProcessError as e:
            err_output = getattr(e, 'stderr', '') or ''
            out_output = getattr(e, 'stdout', '') or ''
            full_out = (err_output + out_output).lower()
            
            logging.error(f"Failed to synchronize code: {e}. Output: {full_out}")
            
            if "another git process seems to be running" in full_out or "index.lock" in full_out:
                logging.warning("Git lock detected. Forcing lock removal...")
                for lock_file in [".git/index.lock", ".git/FETCH_HEAD.lock"]:
                    if os.path.exists(lock_file):
                        try:
                            os.remove(lock_file)
                            logging.info(f"Deleted stale lock file: {lock_file}")
                        except Exception as rm_err:
                            logging.error(f"Failed to remove {lock_file}: {rm_err}")
    else:
        logging.info(f"Code is already up to date at version: {local_version}")
    return False
