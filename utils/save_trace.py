import json
from pathlib import Path


def save_trace(trace: dict, path: Path) -> None:
    if path.suffix == ".gz" or path.name.endswith(".json.gz"):
        with gzip.open(path, "wt") as f:
            json.dump(trace, f)
    else:
        with open(path, "w") as f:
            json.dump(trace, f)

