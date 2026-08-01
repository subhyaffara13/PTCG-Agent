
def parse_location(location: str) -> tuple[str, list[int]]:
    if location.count(":") < 2:
        raise ValueError("Format should be file:line:column[:end_line:end_column]")
    parts = location.rsplit(":", maxsplit=2)
    start, *rest = parts
    # Note: we must allow drive prefix like `C:` on Windows.
    if start.count(":") < 2:
        return start, [int(p) for p in rest]
    parts = start.rsplit(":", maxsplit=2)
    start, *start_rest = parts
    if start.count(":") < 2:
        return start, [int(p) for p in start_rest + rest]
    raise ValueError("Format should be file:line:column[:end_line:end_column]")

