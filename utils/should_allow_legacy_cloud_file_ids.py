
def should_allow_legacy_cloud_file_ids(
    litellm_params: Optional[Mapping[str, Any]] = None,
) -> bool:
    value = None
    if isinstance(litellm_params, Mapping):
        trusted_model_credentials = litellm_params.get(
            "_litellm_internal_model_credentials"
        )
        if isinstance(trusted_model_credentials, _MAPPING_PROXY_TYPE):
            value = cast(Mapping[str, Any], trusted_model_credentials).get(
                "allow_legacy_cloud_file_ids"
            )

    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return False

