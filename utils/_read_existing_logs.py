
import json
from pathlib import Path

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


