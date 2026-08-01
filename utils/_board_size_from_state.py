
def _board_size_from_state(state: Mapping[str, Any]) -> int | None:
    board_size = state.get("board_size")
    if isinstance(board_size, int):
        return board_size
    if isinstance(board_size, str) and board_size.isdigit():
        return int(board_size)
    board_grid = state.get("board_grid")
    if isinstance(board_grid, list) and board_grid:
        return len(board_grid)
    return None

