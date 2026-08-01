
def _get_team(turn: int) -> str:
    """Return the team name for a given turn index."""
    return "BLUE" if turn in (0, 1) else "YELLOW"

