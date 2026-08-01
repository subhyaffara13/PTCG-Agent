
def team_call_validation_checks(
    prisma_client: Optional[PrismaClient],
    data: TeamMemberAddRequest,
    premium_user: bool,
):
    if prisma_client is None:
        raise HTTPException(status_code=500, detail={"error": "No db connected"})

    if data.team_id is None:
        raise HTTPException(status_code=400, detail={"error": "No team id passed in"})

    if data.member is None:
        raise HTTPException(
            status_code=400, detail={"error": "No member/members passed in"}
        )

    try:
        _check_team_member_admin_add(
            member=data.member,
            premium_user=premium_user,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

