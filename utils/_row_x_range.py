
def _row_x_range(y: int, board_size: int) -> tuple[int, int]:
    """Return [start_x, end_x) of playable cells in row y."""
    diameter = board_size * 2 - 1
    if y < board_size:
        return 0, board_size + y
    return y - board_size + 1, diameter

