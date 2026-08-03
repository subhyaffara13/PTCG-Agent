import json
from typing import Any, Dict
from pathlib import Path


def load_donts(donts_file: Path) -> Dict[str, Any]:
    data = {
        "deck_donts": [],
        "behavior_donts": []
    }
    if donts_file.exists():
        try:
            loaded = json.loads(donts_file.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                data.update(loaded)
        except json.JSONDecodeError:
            pass
    if "deck_donts" not in data:
        data["deck_donts"] = []
    if "behavior_donts" not in data:
        data["behavior_donts"] = []
    return data

