import os
from typing import Any
from pathlib import Path


def register_cleanup_lock_removal(lock_path: Path, register: Any) -> Any:
    """Register a cleanup function for removing a lock."""
    pid = os.getpid()

    def cleanup_on_exit(lock_path: Path = lock_path, original_pid: int = pid) -> None:
        current_pid = os.getpid()
        if current_pid != original_pid:
            # fork
            return
        try:
            lock_path.unlink()
        except OSError:
            pass

    return register(cleanup_on_exit)

