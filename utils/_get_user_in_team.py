
def _get_user_in_team(
    team_table: LiteLLM_TeamTableCachedObj, user_id: Optional[str]
) -> Optional[Member]:
    if user_id is None:
        return None
    for member in team_table.members_with_roles:
        if member.user_id is not None and member.user_id == user_id:
            return member

    return None

