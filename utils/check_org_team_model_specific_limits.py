
def check_org_team_model_specific_limits(
    teams: List[LiteLLM_TeamTable],
    org_table: LiteLLM_OrganizationTable,
    data: Union[NewTeamRequest, UpdateTeamRequest],
) -> None:
    """
    Check if the organization team is allocating model specific limits. If so, raise an error if we're overallocating.
    """

    # Get org limits from budget table if available
    entity_rpm_limit = None
    entity_tpm_limit = None
    entity_model_rpm_limit_dict = {}
    entity_model_tpm_limit_dict = {}

    if org_table.litellm_budget_table is not None:
        entity_rpm_limit = org_table.litellm_budget_table.rpm_limit
        entity_tpm_limit = org_table.litellm_budget_table.tpm_limit

    if org_table.metadata:
        entity_model_rpm_limit_dict = org_table.metadata.get("model_rpm_limit", {})
        entity_model_tpm_limit_dict = org_table.metadata.get("model_tpm_limit", {})

    _check_team_model_specific_limits(
        teams=teams,
        data=data,
        entity_rpm_limit=entity_rpm_limit,
        entity_tpm_limit=entity_tpm_limit,
        entity_model_rpm_limit_dict=entity_model_rpm_limit_dict,
        entity_model_tpm_limit_dict=entity_model_tpm_limit_dict,
        entity_type="organization",
    )

