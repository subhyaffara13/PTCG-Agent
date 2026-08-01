
def _get_base_model_from_metadata(model_call_details=None):
    if model_call_details is None:
        return None
    litellm_params = model_call_details.get("litellm_params", {})
    if litellm_params is not None:
        _base_model = litellm_params.get("base_model", None)
        if _base_model is not None:
            return _base_model
        metadata = litellm_params.get("metadata") or {}

        _get_base_model_from_litellm_call_metadata = getattr(
            sys.modules[__name__], "_get_base_model_from_litellm_call_metadata"
        )
        base_model_from_metadata = _get_base_model_from_litellm_call_metadata(
            metadata=metadata
        )
        if base_model_from_metadata is not None:
            return base_model_from_metadata

        # Also check litellm_metadata (used by Responses API and other generic API calls)
        litellm_metadata = litellm_params.get("litellm_metadata", {})
        _get_base_model_from_litellm_call_metadata = getattr(
            sys.modules[__name__], "_get_base_model_from_litellm_call_metadata"
        )
        return _get_base_model_from_litellm_call_metadata(metadata=litellm_metadata)
    return None

