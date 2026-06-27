import os
import glob
import logging
from typing import List

logger = logging.getLogger("LogPruner")

def prune_logs(log_dir: str = "logs", max_files: int = 1000) -> None:
    """
    Scans the log directory for game JSON logs and deletes the oldest ones
    if the total count exceeds max_files. This enforces a sliding window
    memory constraint on PyTorch Analytics.
    """
    if not os.path.exists(log_dir):
        return

    # Find all generated game logs (action, reasoning, variance, steps)
    patterns = [
        "action_game_*.json",
        "reasoning_game_*.json",
        "variance_baseline_*.json",
        "steps_*.json"
    ]
    
    all_files: List[str] = []
    for pattern in patterns:
        all_files.extend(glob.glob(os.path.join(log_dir, pattern)))

    # Sort files by modification time (oldest first)
    all_files.sort(key=os.path.getmtime)

    # If we have more files than allowed, prune the oldest ones
    if len(all_files) > max_files:
        files_to_delete = all_files[:-max_files]
        logger.info(f"Log Pruner active: Found {len(all_files)} logs. Deleting oldest {len(files_to_delete)} to maintain sliding window of {max_files}.")
        
        deleted_count = 0
        for fpath in files_to_delete:
            try:
                os.remove(fpath)
                deleted_count += 1
            except Exception as e:
                logger.warning(f"Failed to delete {fpath}: {e}")
                
        logger.info(f"Log Pruner finished. Deleted {deleted_count} files.")
    else:
        logger.info(f"Log Pruner: {len(all_files)} logs found. Well under the {max_files} limit. No pruning needed.")
