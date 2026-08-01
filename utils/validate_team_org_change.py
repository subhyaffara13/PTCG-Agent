
def validate_team_org_change(
    team: LiteLLM_TeamTable,
    organization: LiteLLM_OrganizationTableWithMembers,
    llm_router: Router,
    is_proxy_admin: bool = False,
) -> bool:
    """
    Validate that a team can be moved to an organization.

    - The org must have access to the team's models
    - The team budget cannot be greater than the org max_budget
    - For non-proxy-admins: all team members must already be org members
    - The team's tpm/rpm limit must be less than the org's tpm/rpm limit

    Proxy admins bypass the membership check and instead trigger auto-add of
    missing members (handled by the caller). This supports SSO/Entra setups
    where org membership tables are empty but proxy admins still need to group
    teams under orgs for budget/model governance.
    """

    # If the team's organization is the same as the new organization, return True
    # Since no changes are being made
    if team.organization_id == organization.organization_id:
        return True

    # Check if the org has access to the team's models
    if len(organization.models) > 0:
        if SpecialModelNames.all_proxy_models.value in organization.models:
            pass
        elif team.models is None or len(team.models) == 0:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Cannot move team to organization. Team has access to all proxy models, but the organization does not."
                },
            )
        else:
            for model in team.models:
                can_org_access_model(
                    model=model,
                    org_object=organization,
                    llm_router=llm_router,
                )

    # Check if the team's budget is less than the org's max_budget
    if (
        team.max_budget
        and organization.litellm_budget_table
        and organization.litellm_budget_table.max_budget
        and team.max_budget > organization.litellm_budget_table.max_budget
    ):
        raise HTTPException(
            status_code=403,
            detail={
                "error": f"Cannot move team to organization. Team has max_budget {team.max_budget} that is greater than the organization's max_budget {organization.litellm_budget_table.max_budget}."
            },
        )

    # For non-proxy-admins, require all team members to already be org members.
    # This prevents a team admin from moving their team into an arbitrary org and
    # thereby injecting members into that org without org admin approval.
    if not is_proxy_admin:
        team_members = [m.user_id for m in team.members_with_roles]
        org_members = (
            [m.user_id for m in organization.members] if organization.members else []
        )
        not_in_org = [
            m
            for m in team_members
            if m not in org_members and m != SpecialProxyStrings.default_user_id.value
        ]
        if len(not_in_org) > 0:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": f"Cannot move team to organization. Team has user_id {not_in_org} that is not a member of the organization."
                },
            )

    # Check if the team's tpm/rpm limit is less than the org's tpm/rpm limit
    if (
        team.tpm_limit
        and organization.litellm_budget_table
        and organization.litellm_budget_table.tpm_limit
        and team.tpm_limit > organization.litellm_budget_table.tpm_limit
    ):
        raise HTTPException(
            status_code=403,
            detail={
                "error": f"Cannot move team to organization. Team has tpm_limit {team.tpm_limit} that is greater than the organization's tpm_limit {organization.litellm_budget_table.tpm_limit}."
            },
        )
    if (
        team.rpm_limit
        and organization.litellm_budget_table
        and organization.litellm_budget_table.rpm_limit
        and team.rpm_limit > organization.litellm_budget_table.rpm_limit
    ):
        raise HTTPException(
            status_code=403,
            detail={
                "error": f"Cannot move team to organization. Team has rpm_limit {team.rpm_limit} that is greater than the organization's rpm_limit {organization.litellm_budget_table.rpm_limit}."
            },
        )
    return True

