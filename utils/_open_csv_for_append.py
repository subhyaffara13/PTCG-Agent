from typing import Any
from pathlib import Path


def _open_csv_for_append(csv_path: Path) -> tuple[Any, csv.DictWriter]:
    """Open ``games.csv`` for appending; write header if new."""
    new_file = not csv_path.exists()
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    f = csv_path.open("a", newline="")
    writer = csv.DictWriter(f, fieldnames=_CSV_FIELDS)
    if new_file:
        writer.writeheader()
        f.flush()
    return f, writer

