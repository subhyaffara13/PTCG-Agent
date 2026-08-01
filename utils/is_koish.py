
def is_koish(board, c):
    """Check if c is surrounded on all sides by 1 color, and return that color."""
    if board[c] != EMPTY:
        return None
    neighbors = {board[n] for n in NEIGHBORS[c]}
    if len(neighbors) == 1 and EMPTY not in neighbors:
        return list(neighbors)[0]
    else:
        return None

