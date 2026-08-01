
def _cell_to_algebraic(row: int, col: int) -> str:
    """Convert 0-indexed (row, col) to algebraic notation, e.g. (0, 0) -> 'a1'."""
    return f"{string.ascii_lowercase[col]}{row + 1}"

