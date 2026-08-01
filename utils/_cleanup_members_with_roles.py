
def _cleanup_members_with_roles(
    existing_team_row: LiteLLM_TeamTable,
    data: TeamMemberDeleteRequest,
) -> Tuple[bool, List[Member]]:
    """Cleanup members_with_roles list for a team."""
    is_member_in_team = False
    new_team_members: List[Member] = []
    for m in existing_team_row.members_with_roles:
        if (
            data.user_id is not None
            and m.user_id is not None
            and data.user_id == m.user_id
        ):
            is_member_in_team = True
            continue
        elif (
            data.user_email is not None
            and m.user_email is not None
            and data.user_email == m.user_email
        ):
            is_member_in_team = True
            continue
        new_team_members.append(m)
    return is_member_in_team, new_team_members

