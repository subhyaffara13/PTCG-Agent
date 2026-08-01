
def _partner_of(ext: int) -> int:
    return _team_of(ext) * _PLAYERS_PER_TEAM + (1 - ext % _PLAYERS_PER_TEAM)

