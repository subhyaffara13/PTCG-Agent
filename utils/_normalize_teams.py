
def _normalize_teams(teams, team_details):
    """If team_details are a

    Args:
        teams (_type_): _description_
        team_details (_type_): _description_

    Returns:
        _type_: _description_
    """
    if isinstance(team_details, list) and team_details:
        return [
            {
                "team_id": i.get("team_id") or i.get("id"),
                "team_alias": i.get("team_alias"),
            }
            for i in team_details
            if isinstance(i, dict) and (i.get("team_id") or i.get("id"))
        ]
    if isinstance(teams, list):
        return [{"team_id": str(t), "team_alias": None} for t in teams]
    return []

