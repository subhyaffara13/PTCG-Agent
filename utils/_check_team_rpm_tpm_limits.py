
def _check_team_rpm_tpm_limits(
    teams: List[LiteLLM_TeamTable],
    data: Union[NewTeamRequest, UpdateTeamRequest],
    entity_rpm_limit: Optional[int],
    entity_tpm_limit: Optional[int],
    entity_type: str,  # "organization"
) -> None:
    """
    Generic function to check if a team is allocating rpm/tpm limits.
    Raises an error if we're overallocating.
    """
    if teams is not None and len(teams) > 0:
        allocated_tpm = sum(
            team.tpm_limit for team in teams if team.tpm_limit is not None
        )
        allocated_rpm = sum(
            team.rpm_limit for team in teams if team.rpm_limit is not None
        )
    else:
        allocated_tpm = 0
        allocated_rpm = 0

    if (
        data.tpm_limit is not None
        and entity_tpm_limit is not None
        and data.tpm_limit + allocated_tpm > entity_tpm_limit
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Allocated TPM limit={allocated_tpm} + Team TPM limit={data.tpm_limit} is greater than {entity_type} TPM limit={entity_tpm_limit}",
        )
    if (
        data.rpm_limit is not None
        and entity_rpm_limit is not None
        and data.rpm_limit + allocated_rpm > entity_rpm_limit
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Allocated RPM limit={allocated_rpm} + Team RPM limit={data.rpm_limit} is greater than {entity_type} RPM limit={entity_rpm_limit}",
        )

