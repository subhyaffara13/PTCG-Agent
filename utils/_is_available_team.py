
def _is_available_team(team_id: str, user_api_key_dict: UserAPIKeyAuth) -> bool:
    if litellm.default_internal_user_params is None:
        return False
    if "available_teams" in litellm.default_internal_user_params:
        return team_id in litellm.default_internal_user_params["available_teams"]
    return False

