from typing import List

def _get_team_ids_with_key_list_permission_from_objects(
    user_api_key_dict: UserAPIKeyAuth,
    team_objects: List[LiteLLM_TeamTable],
) -> List[str]:
    """Filter team objects to non-admin teams where the caller has /key/list
    permission via team_member_permissions. These teams should grant the
    caller full key visibility (same as a team admin), so other members'
    keys and service account keys (user_id=NULL) are returned."""
    return [
        team.team_id
        for team in team_objects
        if not _is_user_team_admin(user_api_key_dict=user_api_key_dict, team_obj=team)
        and _team_member_has_permission(
            user_api_key_dict=user_api_key_dict,
            team_obj=team,
            permission=KeyManagementRoutes.KEY_LIST.value,
        )
    ]

