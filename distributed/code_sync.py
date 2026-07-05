import subprocess
import os
import logging

def get_local_version():
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get local git version: {e}")
        return None
    except FileNotFoundError:
        logging.warning("Git is not installed or not in repository.")
        return None

def sync_code(master_version) -> bool:
    local_version = get_local_version()
    if local_version and master_version and local_version != master_version:
        logging.info(f"Version mismatch. Local: {local_version}, Master: {master_version}. Pulling...")
        try:
            # Discard local modifications to tracked files
            subprocess.run(['git', 'checkout', '-f'], check=True)
            
            # Remove local copies of auto-updated files to prevent conflicts if they are untracked/modified
            files_to_clean = [
                "models/ppo_actor_critic.pt",
                "agents/deck_new.csv",
                "skills/learned_dos.json",
                "skills/predictor_feedback.json",
                "skills/predictor_weights.json"
            ]
            for f in files_to_clean:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception as clean_err:
                        logging.warning(f"Could not remove {f} before pull: {clean_err}")
            
            subprocess.run(['git', 'pull'], check=True)
            logging.info("Code synchronized successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to pull code: {e}")
    else:
        logging.info("Code is up to date or version info unavailable.")
    return False

def restart_process():
    import sys
    import os
    logging.info("Restarting process to reload updated code and weights...")
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        logging.error(f"os.execv failed: {e}. Exiting process.")
        sys.exit(0)
