import logging
from pathlib import Path
from datetime import datetime, timezone
import shutil

from factory.orchestration_process import (
    _LOG_RETENTION_DAYS,
    _PRUNNABLE_DIRS,
    _PRUNNABLE_PREFIXES,
    _KEEP_FILES,
    logger,
)

def prune_old_logs(log_dir: str = "logs", max_age_days: int = _LOG_RETENTION_DAYS) -> None:
    """Delete per‑game JSON logs and subdirectories older than max_age_days.

    Keeps aggregate logs (orchestration_agent.log, crash_report.log,
    iteration_result.json, eval reports) and model files. Call once at startup
    and optionally schedule daily.
    """
    now = datetime.now(timezone.utc).timestamp()
    cutoff = now - (max_age_days * 86400)
    log_path = Path(log_dir)
    if not log_path.exists():
        return

    pruned_files = 0
    pruned_dirs = 0

    # First pass: prune subdirectories and JSON files
    for entry in list(log_path.iterdir()):
        try:
            # Prune old per‑game subdirectories
            if entry.is_dir() and any(entry.name.startswith(p) for p in _PRUNNABLE_DIRS):
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

            # Prune old per‑game JSON log files
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

    # Second pass: prune any remaining subdirectories inside each game folder
    for entry in list(log_path.iterdir()):
        if entry.is_dir() and entry.name.startswith(_PRUNNABLE_DIRS):
            try:
                shutil.rmtree(entry)
                pruned_dirs += 1
            except Exception:
                pass

    if pruned_files > 0 or pruned_dirs > 0:
        logger.info(
            f"Pruned {pruned_files} log files + {pruned_dirs} log dirs older than {max_age_days}d from {log_dir}/"
        )
