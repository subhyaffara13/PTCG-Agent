import sys
import os
import time
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Log file types that can be pruned (non-critical per-game logs)
_PRUNNABLE_PREFIXES = ("action_game_", "reasoning_game_", "steps_", "variance_game_")
_PRUNNABLE_DIRS = ("deck_test_", "opt_val_", "variance_baseline_", "reasoning_test_", "player_")
_KEEP_FILES = {"orchestration_agent.log", "crash_report.log", "iteration_result.json",
               "eval_report.json", "eval_state.json", "action_log.json", "reasoning_log.json",
               "master_server.log", "check_submissions.log", "best_fitness.json"}
_LOG_RETENTION_DAYS = 3

def prune_old_logs(log_dir: str = "logs", max_age_days: int = _LOG_RETENTION_DAYS):
    """Delete per-game JSON logs and subdirectories older than max_age_days.
    
    Keeps aggregate logs (orchestration_agent.log, crash_report.log,
    iteration_result.json, eval reports) and model files.
    Call once at startup and optionally schedule daily.
    """
    from datetime import datetime, timezone
    import shutil
    
    now = datetime.now(timezone.utc).timestamp()
    cutoff = now - (max_age_days * 86400)
    log_path = Path(log_dir)
    if not log_path.exists():
        return

    pruned_files = 0
    pruned_dirs = 0
    
    for entry in list(log_path.iterdir()):
        try:
            # Prune old per-game subdirectories
            if entry.is_dir() and any(entry.name.startswith(p) for p in _PRUNABLE_DIRS):
                try:
                    dir_time = entry.stat().st_mtime
                    if dir_time < cutoff:
                        shutil.rmtree(entry)
                        pruned_dirs += 1
                except Exception:
                    pass
                continue

            if not entry.is_file():
                continue

            # Keep important aggregate files regardless of age
            if entry.name in _KEEP_FILES or entry.suffix in (".pt", ".pth", ".csv"):
                continue

            # Prune old per-game JSON log files
            if entry.name.startswith(_PRUNNABLE_PREFIXES) and entry.suffix == ".json":
                try:
                    file_time = entry.stat().st_mtime
                    if file_time < cutoff:
                        entry.unlink()
                        pruned_files += 1
                except Exception:
                    pass
        except Exception:
            pass

    # Also prune log subdirectories inside each game subfolder
    for entry in list(log_path.iterdir()):
        if entry.is_dir() and entry.name.startswith(_PRUNNABLE_DIRS):
            try:
                shutil.rmtree(entry)
                pruned_dirs += 1
            except Exception:
                pass

    if pruned_files > 0 or pruned_dirs > 0:
        logger.info(f"Pruned {pruned_files} log files + {pruned_dirs} log dirs older than {max_age_days}d from {log_dir}/")


def script_log_path(script: str) -> str:
    return f"logs/{Path(script).stem}.log"


def launch_processes(scripts: list) -> list:
    processes = []
    for i, script in enumerate(scripts):
        if i > 0:
            time.sleep(15)
        log_path = script_log_path(script)
        try:
            f = open(log_path, "a", encoding="utf-8")
            p = subprocess.Popen([sys.executable, script], stdout=f, stderr=f)
            processes.append((p, f))
            logger.info(f"Started: {script} (PID {p.pid}) -> {log_path}")
        except Exception as e:
            logger.error(f"Failed to start {script}: {e}")
            processes.append((None, None))
    return processes


def monitor_and_restart(processes: list, scripts: list):
    for i, (p, f) in enumerate(processes):
        if p is None or p.poll() is not None:
            logger.warning(f"Sub-task {scripts[i]} stopped. Restarting...")
            if f is not None:
                try:
                    f.close()
                except Exception:
                    pass
            try:
                log_path = script_log_path(scripts[i])
                f = open(log_path, "a", encoding="utf-8")
                p = subprocess.Popen([sys.executable, scripts[i]], stdout=f, stderr=f)
                processes[i] = (p, f)
                logger.info(f"Restarted: {scripts[i]} (PID {p.pid}) -> {log_path}")
            except Exception as e:
                logger.error(f"Failed to restart {scripts[i]}: {e}")
                processes[i] = (None, None)


def cleanup(processes: list):
    logger.info("Cleaning up sub-tasks...")
    # First send terminate to all processes immediately to trigger fast shutdowns
    for p, f in processes:
        if p is not None:
            try:
                p.terminate()
            except Exception:
                pass
                
    # Now wait for them to exit, falling back to force-kill if interrupted
    for p, f in processes:
        if p is None:
            continue
        try:
            p.wait(timeout=2)
        except BaseException:
            try:
                p.kill()
            except Exception:
                pass
        if f is not None:
            try:
                f.close()
            except Exception:
                pass
