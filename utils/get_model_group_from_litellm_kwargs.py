
def get_model_group_from_litellm_kwargs(kwargs: dict) -> Optional[str]:
    _litellm_params = kwargs.get("litellm_params", None) or {}
    _metadata = (
        _litellm_params.get(get_metadata_variable_name_from_kwargs(kwargs)) or {}
    )
    _model_group = _metadata.get("model_group", None)
    if _model_group is not None:
        return _model_group

    return None

