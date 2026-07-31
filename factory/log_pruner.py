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

    # Archive old logs before deletion into compressed zip archives in logs/archive/
    archive_dir = os.path.join(log_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    # Truncate oversized process log files (e.g. master_server.log, run_ppo_trainer_loop.log) if larger than 10MB
    # Note: Repeated error logs are PURGED immediately without archiving to prevent storing error spam!
    for log_name in ["master_server.log", "run_ppo_trainer_loop.log", "run_deck_optimizer_loop.log"]:
        f_path = os.path.join(log_dir, log_name)
        if os.path.exists(f_path):
            try:
                if os.path.getsize(f_path) > 10 * 1024 * 1024:  # 10 MB
                    with open(f_path, "w", encoding="utf-8") as f:
                        f.write(f"--- Log purged & truncated by LogPruner at size limit (10MB) ---\n")
                    logger.info(f"Log Pruner: Purged & truncated oversized process log {log_name} (error spam discarded).")
            except Exception as e:
                logger.warning(f"Could not purge/truncate {log_name}: {e}")

    # If we reach or exceed the limit, archive and prune oldest files down to buffer size
    if len(all_files) >= max_files:
        keep_count = max(100, max_files - 100)
        files_to_delete = all_files[:-keep_count]
        logger.info(f"Log Pruner active: Found {len(all_files)} logs. Archiving & deleting oldest {len(files_to_delete)} to maintain sliding window below limit of {max_files}.")
        
        import zipfile
        import time
        game_arc_name = f"game_logs_{int(time.time())}.zip"
        game_arc_path = os.path.join(archive_dir, game_arc_name)
        
        try:
            with zipfile.ZipFile(game_arc_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for fpath in files_to_delete:
                    zf.write(fpath, arcname=os.path.basename(fpath))
            logger.info(f"Log Pruner: Compressed {len(files_to_delete)} game logs into archive {game_arc_name}")
        except Exception as e:
            logger.warning(f"Failed to create zip archive: {e}")

        deleted_count = 0
        for fpath in files_to_delete:
            try:
                os.remove(fpath)
                deleted_count += 1
            except Exception as e:
                logger.warning(f"Failed to delete {fpath}: {e}")
                
        logger.info(f"Log Pruner finished. Archived and deleted {deleted_count} files.")
    else:
        logger.info(f"Log Pruner: {len(all_files)} logs found (below limit of {max_files}). No pruning needed.")
