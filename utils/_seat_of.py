
def _seat_of(player_id: int, players_per_team: int) -> int:
    return player_id % players_per_team


def _seat_of(player_id: int) -> int:
    return player_id % _PLAYERS_PER_TEAM

