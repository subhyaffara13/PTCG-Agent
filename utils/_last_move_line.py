
def _last_move_line(move_history: list[str]) -> str:
    if not move_history:
        return "This is your first move."
    return f"Your most recent nominated move was: {move_history[-1]}"

