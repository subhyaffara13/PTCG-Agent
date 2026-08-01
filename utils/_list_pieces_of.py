
def _list_pieces_of(
    board: Sequence[Sequence[str]], player_id: int
) -> tuple[list[str], list[str]]:
    """Return (men_squares, king_squares) in algebraic notation for player."""
    man_char = "o" if player_id == 0 else "+"
    king_char = "O" if player_id == 0 else "*"
    men: list[str] = []
    kings: list[str] = []
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            square = f"{chr(ord('a') + c)}{r + 1}"
            if cell == man_char:
                men.append(square)
            elif cell == king_char:
                kings.append(square)
    return men, kings

