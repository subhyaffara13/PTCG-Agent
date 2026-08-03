import json
from pathlib import Path


def load_tensors_data(path: "str | Path") -> "TensorsData":
    """Load calibration tensor ranges from a JSON file written by save_tensors_data()."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Calibration cache not found: {path}")
    if not path.is_file():
        raise ValueError(f"Calibration cache path is not a file: {path}")
    with path.open("r") as f:
        d = json.load(f)
    return TensorsData.from_dict(d)

