import subprocess
from pathlib import Path


def auto_commit_and_push_if_changed():
    """Checks for changes to key factory/logic files, commits, and pushes them to Git."""
    # List of files we want to ensure stay synchronized across all nodes
    target_files = [
        "models/ppo_actor_critic.pt",
        "skills/learned_dos.json",
        "skills/predictor_feedback.json",
        "skills/predictor_weights.json"
    ]
    
    # Filter files that actually exist and have modifications
    files_to_add = []
    for file_str in target_files:
        p = Path(file_str)
        if p.exists():
            # Check if git detects modification/untracked status for this file
            res = _run_git(["git", "status", "--porcelain", file_str], capture_output=True, text=True)
            if res.stdout.strip():
                files_to_add.append(file_str)
                
    if not files_to_add:
        logger.info("No factory updates detected. Skipping Git push.")
        return
        
    logger.info(f"Factory updates detected in: {files_to_add}. Preparing auto-commit and push...")
    try:
        # Add files
        _run_git(["git", "add"] + files_to_add, check=True, capture_output=True, text=True)
        # Commit
        commit_msg = "Auto-update: Factory model/deck/skills update"
        _run_git(["git", "commit", "-m", commit_msg], check=True, capture_output=True, text=True)
        # Push
        try:
            _run_git(["git", "push"], check=True, capture_output=True, text=True)
            logger.info("Factory updates committed and pushed successfully.")
        except subprocess.CalledProcessError as push_err:
            push_err_out = ((getattr(push_err, 'stderr', '') or '') + (getattr(push_err, 'stdout', '') or '')).lower()
            if "fetch first" in push_err_out or "non-fast-forward" in push_err_out or "behind" in push_err_out:
                logger.warning("Master push rejected due to remote changes. Attempting git pull --rebase...")
                try:
                    _run_git(["git", "pull", "--rebase"], check=True, capture_output=True, text=True)
                    _run_git(["git", "push"], check=True, capture_output=True, text=True)
                    logger.info("Factory updates rebased and pushed successfully.")
                except Exception as rebase_err:
                    logger.error(f"Git rebase/push recovery failed: {rebase_err}")
                    raise
            else:
                raise
    except subprocess.CalledProcessError as e:
        err_out = getattr(e, 'stderr', '') or ''
        std_out = getattr(e, 'stdout', '') or ''
        full_out = (err_out + std_out).lower()
        logger.error(f"Git auto-push failed (will retry next check): {e}")
        
        # Auto-fix Git lock issues on master node
        import os
        if "another git process seems to be running" in full_out or "index.lock" in full_out:
            logger.warning("Git lock detected on Master. Forcing lock removal...")
            for lock_file in [".git/index.lock", ".git/FETCH_HEAD.lock"]:
                if os.path.exists(lock_file):
                    try:
                        os.remove(lock_file)
                        logger.info(f"Deleted stale lock file on Master: {lock_file}")
                    except Exception as rm_err:
                        logger.error(f"Failed to remove {lock_file}: {rm_err}")
    except Exception as e:
        logger.error(f"Unexpected error during Git auto-push: {e}")

