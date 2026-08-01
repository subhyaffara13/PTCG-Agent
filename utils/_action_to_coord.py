
def _action_to_coord(action: int, board_size: int) -> str:
    diameter = board_size * 2 - 1
    x = action % diameter
    y = action // diameter
    return f"{chr(ord('a') + x)}{y + 1}"


def _action_to_coord(action: int, board_size: int) -> str:
    row = action // board_size
    col = action % board_size
    return f"{chr(ord('a') + col)}{row + 1}"

