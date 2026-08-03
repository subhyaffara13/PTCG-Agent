import json
from pathlib import Path


def append_to_history(history_file: Path, record: dict):
    history = []
    if history_file.exists():
        try: history = json.loads(history_file.read_text(encoding="utf-8").strip())
        except: pass
    history.append(record)
    try: history_file.write_text(json.dumps(history, indent=2), encoding="utf-8")
    except: pass

