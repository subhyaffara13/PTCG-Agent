
def _player_info(player_id: int) -> tuple[str, str, str]:
    """Return (display_name, board_code, connect_goal_text)."""
    if player_id == 0:
        return "Player X", "x", "the TOP edge to the BOTTOM edge"
    return "Player O", "o", "the LEFT edge to the RIGHT edge"

