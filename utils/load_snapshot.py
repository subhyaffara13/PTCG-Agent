import json
from typing import Dict, Optional

def load_snapshot() -> Optional[Dict[str, Dict]]:
    if not SNAPSHOT_FILE.exists():
        return None
    try:
        with SNAPSHOT_FILE.open() as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

