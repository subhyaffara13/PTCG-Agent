
def _team_role(turn: int) -> tuple[str, str]:
    """Return ``(my_role, opp_role)`` as the lowercase role values used in
    ``observation.roles`` for this turn."""
    if turn in (0, 1):
        return "blue", "yellow"
    return "yellow", "blue"

