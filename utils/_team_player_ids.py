
def _team_player_ids(team: int, players_per_team: int) -> list[int]:
    base = team * players_per_team
    return [base + s for s in range(players_per_team)]


def _team_player_ids(team: int) -> list[int]:
    base = team * _PLAYERS_PER_TEAM
    return [base + s for s in range(_PLAYERS_PER_TEAM)]

