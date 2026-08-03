import os

def truncate_large_logs(log_dir):
    for log_name in ["master_server.log", "run_ppo_trainer_loop.log", "run_deck_optimizer_loop.log"]:
        f_path = os.path.join(log_dir, log_name)
        if os.path.exists(f_path):
            try:
                if os.path.getsize(f_path) > 10 * 1024 * 1024:
                    with open(f_path, "w", encoding="utf-8") as f:
                        f.write(f"--- Log purged & truncated by LogPruner at size limit (10MB) ---\n")
                    logger.info(f"Log Pruner: Purged & truncated oversized process log {log_name} (error spam discarded).")
            except Exception as e:
                logger.warning(f"Could not purge/truncate {log_name}: {e}")

