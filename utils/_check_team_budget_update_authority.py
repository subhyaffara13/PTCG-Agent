
def _check_team_budget_update_authority(
    data: UpdateTeamRequest,
    user_api_key_dict: UserAPIKeyAuth,
    existing_team_max_budget: Optional[float],
) -> None:
    """
    Restrict who can grow a standalone team's spend ceiling on /team/update.

    A team admin (already authorized via _verify_team_access) may keep or lower
    the team budget, but only a proxy admin may grow it - by raising max_budget
    above the team's current value or by removing the cap (setting it to None).
    Setting a finite budget on a team that has no cap is a restriction and is
    allowed. Org-scoped teams are governed by _check_org_team_limits().
    """
    if user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN:
        return
    if existing_team_max_budget is None:
        return

    budget_explicitly_set = "max_budget" in (
        getattr(data, "model_fields_set", None) or set()
    )
    if budget_explicitly_set and data.max_budget is None:
        raise HTTPException(
            status_code=403,
            detail={
                "error": f"Only a proxy admin can remove a team's max_budget. Team's current max_budget={existing_team_max_budget}."
            },
        )

    if data.max_budget is not None and data.max_budget > existing_team_max_budget:
        raise HTTPException(
            status_code=403,
            detail={
                "error": f"Only a proxy admin can raise a team's max_budget. Team's current max_budget={existing_team_max_budget}, requested={data.max_budget}."
            },
        )

