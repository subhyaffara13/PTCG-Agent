from typing import Optional

def use_custom_pricing_for_model(litellm_params: Optional[dict]) -> bool:
    """
    Check if the model uses custom pricing

    Returns True if any of `SPECIAL_MODEL_INFO_PARAMS` are present in `litellm_params` or `model_info`
    """
    if litellm_params is None:
        return False

    # Check litellm_params using set intersection (only check keys that exist in both)
    matching_keys = _CUSTOM_PRICING_KEYS & litellm_params.keys()
    for key in matching_keys:
        if litellm_params.get(key) is not None:
            return True

    # Check model_info from metadata or litellm_metadata (generic_api_call routes
    # like /responses and /messages store model_info under litellm_metadata)
    for metadata_key in ("metadata", "litellm_metadata"):
        metadata: dict = litellm_params.get(metadata_key, {}) or {}
        model_info: dict = metadata.get("model_info", {}) or {}

        if model_info:
            matching_keys = _CUSTOM_PRICING_KEYS & model_info.keys()
            for key in matching_keys:
                if model_info.get(key) is not None:
                    return True

    return False

