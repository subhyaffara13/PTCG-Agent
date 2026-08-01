
def _list_player_squares(board: Sequence[Sequence[str]], piece_char: str) -> list[str]:
    """Return algebraic squares (e.g. 'a7') holding ``piece_char`` pieces.

    ``board[0]`` is the top visual row (rank == len(board)).
    """
    rows = len(board)
    squares: list[str] = []
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == piece_char:
                squares.append(f"{chr(ord('a') + c)}{rows - r}")
    return squares

