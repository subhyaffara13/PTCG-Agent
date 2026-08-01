
def _format_piece_line_counts(
    board: Sequence[Sequence[str]], my_piece: str,
) -> str:
    """For each of the player's pieces, list piece counts on its 4 lines.

    A LoA piece moves EXACTLY this many squares along the chosen line, so
    pre-computing these counts saves the model from a tedious step that's
    easy to get wrong.
    """
    if not board:
        return "(unavailable)"
    n = len(board[0])
    # Row r (1-indexed), column f (0=a). board[r-1][f].
    row_count = [sum(1 for cell in board[r] if cell != ".") for r in range(n)]
    col_count = [
        sum(1 for r in range(n) if board[r][c] != ".") for c in range(n)
    ]
    ne_count: dict[int, int] = {}  # key = rank - file (constant on '/' diagonal)
    nw_count: dict[int, int] = {}  # key = rank + file (constant on '\' diagonal)
    for r in range(n):
        for c in range(n):
            if board[r][c] == ".":
                continue
            ne_count[(r + 1) - (c + 1)] = ne_count.get((r + 1) - (c + 1), 0) + 1
            nw_count[(r + 1) + (c + 1)] = nw_count.get((r + 1) + (c + 1), 0) + 1

    lines = []
    for r in range(n - 1, -1, -1):
        for c in range(n):
            if board[r][c] != my_piece:
                continue
            sq = f"{chr(ord('a') + c)}{r + 1}"
            row = row_count[r]
            col = col_count[c]
            ne = ne_count.get((r + 1) - (c + 1), 0)
            nw = nw_count.get((r + 1) + (c + 1), 0)
            lines.append(f"  {sq}: row={row}, col={col}, /={ne}, \\={nw}")
    return "\n".join(lines) if lines else "  (no pieces)"

