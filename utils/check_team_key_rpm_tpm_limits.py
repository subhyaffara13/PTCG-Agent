
def check_team_key_rpm_tpm_limits(
    keys: List[LiteLLM_VerificationToken],
    team_table: LiteLLM_TeamTableCachedObj,
    data: Union[GenerateKeyRequest, UpdateKeyRequest],
) -> None:
    """
    Check if the team key is allocating rpm/tpm limits. If so, raise an error if we're overallocating.
    """
    _check_key_rpm_tpm_limits(
        keys=keys,
        data=data,
        entity_rpm_limit=team_table.rpm_limit,
        entity_tpm_limit=team_table.tpm_limit,
        entity_type="team",
    )

