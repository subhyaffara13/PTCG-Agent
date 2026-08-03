from typing import List

def team_member_add_duplication_check(
    data: TeamMemberAddRequest,
    existing_team_row: LiteLLM_TeamTable,
):
    """
    Check if a member already exists in the team.
    This check is done BEFORE we create/fetch the user, so it only prevents
    obvious duplicates where both user_id and user_email match exactly.
    """

    invalid_team_members = []

    def _check_member_duplication(member: Member):
        if member.user_id is not None:
            for existing_member in existing_team_row.members_with_roles:
                if existing_member.user_id == member.user_id:
                    invalid_team_members.append(member)

        # Check by user_email if provided
        if member.user_email is not None:
            for existing_member in existing_team_row.members_with_roles:
                if existing_member.user_email == member.user_email:
                    invalid_team_members.append(member)

    # First, populate the invalid_team_members list by checking for duplicates
    if isinstance(data.member, Member):
        _check_member_duplication(data.member)
    elif isinstance(data.member, List):
        for m in data.member:
            _check_member_duplication(m)

    # Then check the populated list and raise exceptions if needed
    if isinstance(data.member, list) and len(invalid_team_members) == len(data.member):
        raise ProxyException(
            message=f"All users are already in team. Existing members={existing_team_row.members_with_roles}",
            type=ProxyErrorTypes.team_member_already_in_team,
            param="member",
            code="400",
        )
    elif isinstance(data.member, Member) and len(invalid_team_members) == 1:
        raise ProxyException(
            message=f"User already in team. Member: user_id={data.member.user_id}, user_email={data.member.user_email}. Existing members={existing_team_row.members_with_roles}",
            type=ProxyErrorTypes.team_member_already_in_team,
            param="member",
            code="400",
        )
    elif len(invalid_team_members) > 0:
        verbose_proxy_logger.info(
            f"Some users are already in team. Existing members={existing_team_row.members_with_roles}. Duplicate members={invalid_team_members}",
        )

