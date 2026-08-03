from typing import Any

def _infer_alignments(headers: list[str], rows: list[list[Any]]) -> dict[str, str]:
    """Return ``{"col": "right"}`` for columns where every non-None value is numeric."""
    result: dict[str, str] = {}
    for c, h in enumerate(headers):
        if all(row[c] is None or (isinstance(row[c], (int, float)) and not isinstance(row[c], bool)) for row in rows):
            result[h] = "right"
    return result

