
def _initial_tile(x, y, board_size):
    return None if _quadrant_of(x, y, board_size) == "NW" else "LOCKED"

