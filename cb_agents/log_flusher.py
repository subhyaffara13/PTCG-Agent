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
                    raise TimeoutError(f"Failed to acquire lock on {self.lockfile} within {self.timeout}s")
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



from utils.flush_reasoning_logs import flush_reasoning_logs


from utils._read_existing_logs import _read_existing_logs
