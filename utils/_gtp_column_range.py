
def _gtp_column_range(board_size: int | None) -> str:
    """Return compact GTP column guidance for a square Go board."""
    if board_size is None or board_size <= 0:
        return "the columns shown in the board state"
    columns = _GTP_COLUMNS[:board_size]
    if board_size <= 8:
        return f"A-{columns[-1].upper()}"
    if board_size == 9:
        return "A-H,J"
    return f"A-H,J-{columns[-1].upper()}"

