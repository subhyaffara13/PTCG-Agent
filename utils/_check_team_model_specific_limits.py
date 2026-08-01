
def _check_team_model_specific_limits(
    teams: List[LiteLLM_TeamTable],
    data: Union[NewTeamRequest, UpdateTeamRequest],
    entity_rpm_limit: Optional[int],
    entity_tpm_limit: Optional[int],
    entity_model_rpm_limit_dict: Dict[str, int],
    entity_model_tpm_limit_dict: Dict[str, int],
    entity_type: str,  # "organization"
) -> None:
    """
    Generic function to check if a team is allocating model specific limits.
    Raises an error if we're overallocating.
    """
    model_rpm_limit = getattr(data, "model_rpm_limit", None) or (
        data.metadata.get("model_rpm_limit", None) if data.metadata else None
    )
    model_tpm_limit = getattr(data, "model_tpm_limit", None) or (
        data.metadata.get("model_tpm_limit", None) if data.metadata else None
    )
    if model_rpm_limit is None and model_tpm_limit is None:
        return

    # get total model specific tpm/rpm limit
    model_specific_rpm_limit: Dict[str, int] = {}
    model_specific_tpm_limit: Dict[str, int] = {}

    for team in teams:
        if team.metadata and team.metadata.get("model_rpm_limit", None) is not None:
            for model, rpm_limit in team.metadata.get("model_rpm_limit", {}).items():
                model_specific_rpm_limit[model] = (
                    model_specific_rpm_limit.get(model, 0) + rpm_limit
                )
        if team.metadata and team.metadata.get("model_tpm_limit", None) is not None:
            for model, tpm_limit in team.metadata.get("model_tpm_limit", {}).items():
                model_specific_tpm_limit[model] = (
                    model_specific_tpm_limit.get(model, 0) + tpm_limit
                )

    if model_rpm_limit is not None:
        for model, rpm_limit in model_rpm_limit.items():
            if (
                entity_rpm_limit is not None
                and model_specific_rpm_limit.get(model, 0) + rpm_limit
                > entity_rpm_limit
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Allocated RPM limit={model_specific_rpm_limit.get(model, 0)} + Team RPM limit={rpm_limit} is greater than {entity_type} RPM limit={entity_rpm_limit}",
                )
            elif entity_model_rpm_limit_dict:
                entity_model_specific_rpm_limit = entity_model_rpm_limit_dict.get(model)
                if (
                    entity_model_specific_rpm_limit
                    and model_specific_rpm_limit.get(model, 0) + rpm_limit
                    > entity_model_specific_rpm_limit
                ):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Allocated RPM limit={model_specific_rpm_limit.get(model, 0)} + Team RPM limit={rpm_limit} is greater than {entity_type} RPM limit={entity_model_specific_rpm_limit}",
                    )

    if model_tpm_limit is not None:
        for model, tpm_limit in model_tpm_limit.items():
            if (
                entity_tpm_limit is not None
                and model_specific_tpm_limit.get(model, 0) + tpm_limit
                > entity_tpm_limit
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Allocated TPM limit={model_specific_tpm_limit.get(model, 0)} + Team TPM limit={tpm_limit} is greater than {entity_type} TPM limit={entity_tpm_limit}",
                )
            elif entity_model_tpm_limit_dict:
                entity_model_specific_tpm_limit = entity_model_tpm_limit_dict.get(model)
                if (
                    entity_model_specific_tpm_limit
                    and model_specific_tpm_limit.get(model, 0) + tpm_limit
                    > entity_model_specific_tpm_limit
                ):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Allocated TPM limit={model_specific_tpm_limit.get(model, 0)} + Team TPM limit={tpm_limit} is greater than {entity_type} TPM limit={entity_model_specific_tpm_limit}",
                    )

