
def _write_trace(path: str, data: dict[str, Any]) -> None:
    """Write trace data to a gzipped JSON file."""
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(data, f)

