
def _team_member_has_permission(
    user_api_key_dict: UserAPIKeyAuth,
    team_obj: LiteLLM_TeamTable,
    permission: str,
) -> bool:
    """Check if a non-admin team member has a specific permission on a team."""
    if not team_obj.team_member_permissions:
        return False
    if permission not in team_obj.team_member_permissions:
        return False
    for member in team_obj.members_with_roles:
        if member.user_id is not None and member.user_id == user_api_key_dict.user_id:
            return True
    return False

