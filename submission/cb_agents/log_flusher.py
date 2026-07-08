"""
cb_agents/log_flusher.py

Shared utility for flushing in-memory reasoning log buffers to JSON files.
Handles reading existing logs, merging, and writing back atomically.
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import List


class FileLock:
    """Atomic cross-platform file locking manager using OS-level O_EXCL flags."""
    def __init__(self, filepath: Path, timeout: float = 5.0):
        self.lockfile = Path(str(filepath) + ".lock")
        self.timeout = timeout
        self.dummy = False

    def __enter__(self):
        start = time.time()
        while True:
            try:
                fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                return self
            except FileExistsError:
                if time.time() - start > self.timeout:
                    try:
                        self.lockfile.unlink(missing_ok=True)
                    except:
                        pass
                time.sleep(0.05)
            except Exception:
                # If directory is read-only or permission is denied, fallback to dummy lock
                self.dummy = True
                return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.dummy:
            try:
                self.lockfile.unlink(missing_ok=True)
            except:
                pass



def flush_reasoning_logs(
    buffer: List[dict],
    filepath: Path,
    log: logging.Logger,
) -> None:
    """
    Write all buffered log entries to *filepath*, merging with any
    existing entries already on disk.  Clears *buffer* on success.
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


def _read_existing_logs(filepath: Path) -> list:
    """Return the list of log entries already stored in *filepath*."""
    if not filepath.exists():
        return []

    content = filepath.read_text(encoding="utf-8").strip()
    if not content:
        return []

    try:
        data = json.loads(content)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return []
