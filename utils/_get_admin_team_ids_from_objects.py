from typing import List

def _get_admin_team_ids_from_objects(
    user_api_key_dict: UserAPIKeyAuth,
    team_objects: List[LiteLLM_TeamTable],
) -> List[str]:
    """Filter team objects to those where the user is an admin."""
    return [
        team.team_id
        for team in team_objects
        if _is_user_team_admin(user_api_key_dict=user_api_key_dict, team_obj=team)
    ]

