from typing import List

def _get_member_team_ids_from_objects(
    user_api_key_dict: UserAPIKeyAuth,
    team_objects: List[LiteLLM_TeamTable],
) -> List[str]:
    """Filter team objects to those where the user is a member (any role)."""
    return [
        team.team_id
        for team in team_objects
        if any(
            member.user_id is not None and member.user_id == user_api_key_dict.user_id
            for member in team.members_with_roles
        )
    ]

