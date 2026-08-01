
def _get_opponent_element_type(game_state) -> str:
    """Get the opponent's active Pokemon's element type."""
    try:
        active = getattr(game_state, 'opponent_active', None)
        if isinstance(active, dict):
            return active.get("element_type", "") or active.get("type", "") or ""
    except Exception:
        pass
    return ""


def _get_opponent_element_type(game_state) -> str:
    """Get the opponent's active Pokemon's element type."""
    try:
        active = getattr(game_state, 'opponent_active', None)
        if isinstance(active, dict):
            return active.get("element_type", "") or active.get("type", "") or ""
    except Exception:
        pass
    return ""

