import json
from pathlib import Path


def read_fitness(path: str, key: str) -> float:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return float(data.get(key, -9999.0))
    except Exception:
        return -9999.0

