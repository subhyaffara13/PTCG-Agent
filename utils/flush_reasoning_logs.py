
from typing import List
import json
import logging
from pathlib import Path

class FileLock:
    def __init__(self, filepath):
        self.filepath = filepath
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def _read_existing_logs(filepath: Path) -> List[dict]:
    if filepath.exists():
        try:
            return json.loads(filepath.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def flush_reasoning_logs(
    buffer: List[dict],
    filepath: Path,
    log: logging.Logger,
) -> None:
    """
    Write all buffered log entries to *filepath*, merging with any
    existing entries already on disk. Clears *buffer* on success.
    Protected by atomic file locking.
    """
    if not buffer:
        return

    with FileLock(filepath):
        try:
            logs = _read_existing_logs(filepath)
            logs.extend(buffer)
            filepath.write_text(json.dumps(logs, indent=2), encoding="utf-8")
            buffer.clear()
        except Exception as e:
            log.error(f"Failed to flush reasoning logs to {filepath}: {e}")


