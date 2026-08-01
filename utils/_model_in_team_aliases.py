
def _model_in_team_aliases(
    model: str, team_model_aliases: Optional[Dict[str, str]] = None
) -> bool:
    """
    Returns True if `model` being accessed is an alias of a team model

    - `model=gpt-4o`
    - `team_model_aliases={"gpt-4o": "gpt-4o-team-1"}`
        - returns True

    - `model=gp-4o`
    - `team_model_aliases={"o-3": "o3-preview"}`
        - returns False
    """
    if team_model_aliases:
        if model in team_model_aliases:
            return True
    return False

