
def _abs_to_point(player_id: int, abs_pos: int) -> int:
    """OpenSpiel absolute pos (0..23) -> player-relative point (1..24).

    Player O numbers points 1..24 in increasing OpenSpiel order; player X
    uses the mirror, so their 1-point is OpenSpiel pos 23.
    """
    if player_id == 1:
        return abs_pos + 1
    return 24 - abs_pos

