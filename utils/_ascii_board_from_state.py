
def _ascii_board_from_state(state: Mapping[str, Any]) -> str:
    board = state.get("ascii_board")
    if isinstance(board, str) and board.strip():
        return board
    return "Not available in this observation."

