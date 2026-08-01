
def _read_trace(path: str) -> dict[str, Any]:
    """Read trace data from a JSON file (gzipped or not)."""
    if path.endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(path) as f:
            return json.load(f)

