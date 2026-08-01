
def list_episodes_for_team(team_id: int) -> dict[str, Any]:
    return __list_episodes({"TeamId": team_id})

