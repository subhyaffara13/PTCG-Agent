
def _algebraic_to_cell(text: str) -> tuple[int, int] | None:
    """Convert 'a1' / 'J10' to 0-indexed (row, col), or None if unparseable."""
    match = _CELL_RE.search(text)
    if not match:
        return None
    col = string.ascii_lowercase.index(match.group(1).lower())
    row = int(match.group(2)) - 1
    return row, col

