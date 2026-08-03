from typing import Dict, Optional

def initialize_standard_callback_dynamic_params(
    kwargs: Optional[Dict] = None,
) -> StandardCallbackDynamicParams:
    """
    Initialize the standard callback dynamic params from the kwargs

    checks supported request callback params in kwargs and sets the corresponding attributes in StandardCallbackDynamicParams
    """

    standard_callback_dynamic_params = StandardCallbackDynamicParams()
    if kwargs:
        # 1. Check top-level kwargs
        for param in _supported_callback_params:
            if param in _request_blocked_callback_params:
                continue
            if param in kwargs:
                _param_value = kwargs.get(param)
                validate_no_callback_env_reference(
                    param, _param_value, source="request body"
                )
                standard_callback_dynamic_params[param] = _param_value  # type: ignore

        # 2. Fallback: check "metadata" or "litellm_params" -> "metadata"
        metadata = (kwargs.get("metadata") or {}).copy()
        litellm_params = kwargs.get("litellm_params") or {}
        if isinstance(litellm_params, dict):
            metadata.update(litellm_params.get("metadata") or {})

        if isinstance(metadata, dict):
            for param in _supported_callback_params:
                if param in _request_blocked_callback_params:
                    continue
                if param not in standard_callback_dynamic_params and param in metadata:
                    _param_value = metadata.get(param)
                    validate_no_callback_env_reference(
                        param, _param_value, source="metadata"
                    )
                    standard_callback_dynamic_params[param] = _param_value  # type: ignore

    return standard_callback_dynamic_params

