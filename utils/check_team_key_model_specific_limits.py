from typing import List, Union

def check_team_key_model_specific_limits(
    keys: List[LiteLLM_VerificationToken],
    team_table: LiteLLM_TeamTableCachedObj,
    data: Union[GenerateKeyRequest, UpdateKeyRequest],
) -> None:
    """
    Check if the team key is allocating model specific limits. If so, raise an error if we're overallocating.
    """
    entity_model_rpm_limit_dict = {}
    entity_model_tpm_limit_dict = {}
    if team_table.metadata:
        entity_model_rpm_limit_dict = team_table.metadata.get("model_rpm_limit", {})
        entity_model_tpm_limit_dict = team_table.metadata.get("model_tpm_limit", {})

    _check_key_model_specific_limits(
        keys=keys,
        data=data,
        entity_rpm_limit=team_table.rpm_limit,
        entity_tpm_limit=team_table.tpm_limit,
        entity_model_rpm_limit_dict=entity_model_rpm_limit_dict,
        entity_model_tpm_limit_dict=entity_model_tpm_limit_dict,
        entity_type="team",
    )

