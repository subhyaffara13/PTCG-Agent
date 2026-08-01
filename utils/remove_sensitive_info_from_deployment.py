
def remove_sensitive_info_from_deployment(
    deployment_dict: dict,
    excluded_keys: Optional[Set[str]] = None,
) -> dict:
    """
    Removes sensitive information from a deployment dictionary.

    Args:
        deployment_dict (dict): The deployment dictionary to remove sensitive information from.
        excluded_keys (Optional[Set[str]]): Set of keys that should not be masked (exact match).

    Returns:
        dict: The modified deployment dictionary with sensitive information removed.
    """
    deployment_dict["litellm_params"].pop("api_key", None)
    deployment_dict["litellm_params"].pop("client_secret", None)
    deployment_dict["litellm_params"].pop("vertex_credentials", None)
    deployment_dict["litellm_params"].pop("vertex_ai_credentials", None)
    deployment_dict["litellm_params"].pop("aws_access_key_id", None)
    deployment_dict["litellm_params"].pop("aws_secret_access_key", None)

    # Rate-limit config fields must never be masked — they are integers, not credentials.
    # The field names contain "key" which matches the masker's sensitive pattern, so we
    # explicitly exclude them here rather than widening the global non_sensitive_overrides.
    _rate_limit_config_keys = {
        "default_api_key_tpm_limit",
        "default_api_key_rpm_limit",
    }
    _excluded = (excluded_keys or set()) | _rate_limit_config_keys

    deployment_dict["litellm_params"] = SENSITIVE_DATA_MASKER.mask_dict(
        deployment_dict["litellm_params"], excluded_keys=_excluded
    )

    return deployment_dict

