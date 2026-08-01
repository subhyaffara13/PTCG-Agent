
def _coordinate_guidance(board_size: int | None) -> str:
    if board_size is None or board_size <= 0:
        return (
            "Coordinates use GTP notation: column letters shown in "
            'the board state, skipping "I", followed by row numbers starting '
            'from 1.'
        )
    return (
        f"Coordinates use GTP notation for this {board_size}x{board_size} board: "
        f"columns are {_gtp_column_range(board_size)} (the letter \"I\" is "
        f"skipped), and rows are 1-{board_size}."
    )

