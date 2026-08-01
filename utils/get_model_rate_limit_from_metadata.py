
def get_model_rate_limit_from_metadata(
    user_api_key_dict: UserAPIKeyAuth,
    metadata_accessor_key: Literal[
        "team_metadata", "organization_metadata", "project_metadata"
    ],
    rate_limit_key: Literal["model_rpm_limit", "model_tpm_limit"],
) -> Optional[Dict[str, int]]:
    if getattr(user_api_key_dict, metadata_accessor_key):
        return getattr(user_api_key_dict, metadata_accessor_key).get(rate_limit_key)
    return None

