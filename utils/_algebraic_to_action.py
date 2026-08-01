
def _algebraic_to_action(algebraic: str, num_cols: int) -> int | None:
    """Inverse of ``_action_to_algebraic`` ('a7' -> 60 on a 10-wide board)."""
    cell = _algebraic_to_cell(algebraic)
    if cell is None:
        return None
    row, col = cell
    return row * num_cols + col

