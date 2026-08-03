import time
from pathlib import Path


def get_new_file_path(log_dir: Path) -> Path:
    timestamp = int(time.time())
    return log_dir / f"trajectory_{timestamp}.jsonl"

