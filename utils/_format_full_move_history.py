
def _format_full_move_history(state: Mapping[str, Any]) -> str:
    history = state.get("move_history")
    if not history:
        return "None"
    if isinstance(history, list):
        return " ".join(str(move) for move in history) or "None"
    return str(history)

