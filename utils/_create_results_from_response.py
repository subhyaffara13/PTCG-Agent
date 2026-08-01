
def _create_results_from_response(
    members: List[Member],
    response: TeamAddMemberResponse,
) -> List[TeamMemberAddResult]:
    """
    Convert TeamAddMemberResponse into individual TeamMemberAddResult objects
    """
    results: List[TeamMemberAddResult] = []

    for member in members:
        # Find corresponding updated user
        updated_user = None
        for user in response.updated_users:
            if (member.user_id and user.user_id == member.user_id) or (
                member.user_email and user.user_email == member.user_email
            ):
                updated_user = user.model_dump()
                break

        # Find corresponding updated team membership
        updated_team_membership = None
        for tm in response.updated_team_memberships:
            if member.user_id and tm.user_id == member.user_id:
                updated_team_membership = tm.model_dump()
                break

        results.append(
            TeamMemberAddResult(
                user_id=member.user_id,
                user_email=member.user_email,
                success=True,
                updated_user=updated_user,
                updated_team_membership=updated_team_membership,
            )
        )

    return results

