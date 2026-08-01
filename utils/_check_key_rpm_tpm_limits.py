
def _check_key_rpm_tpm_limits(
    keys: List[LiteLLM_VerificationToken],
    data: Union[GenerateKeyRequest, UpdateKeyRequest],
    entity_rpm_limit: Optional[int],
    entity_tpm_limit: Optional[int],
    entity_type: str,  # "team" or "organization"
) -> None:
    """
    Generic function to check if a key is allocating rpm/tpm limits.
    Raises an error if we're overallocating.
    """
    if keys is not None and len(keys) > 0:
        allocated_tpm = sum(key.tpm_limit for key in keys if key.tpm_limit is not None)
        allocated_rpm = sum(key.rpm_limit for key in keys if key.rpm_limit is not None)
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
            detail=f"Allocated TPM limit={allocated_tpm} + Key TPM limit={data.tpm_limit} is greater than {entity_type} TPM limit={entity_tpm_limit}",
        )
    if (
        data.rpm_limit is not None
        and entity_rpm_limit is not None
        and data.rpm_limit + allocated_rpm > entity_rpm_limit
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Allocated RPM limit={allocated_rpm} + Key RPM limit={data.rpm_limit} is greater than {entity_type} RPM limit={entity_rpm_limit}",
        )

