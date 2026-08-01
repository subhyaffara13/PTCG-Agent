
def _model_matches_any_wildcard_pattern_in_list(
    model: str, allowed_model_list: list
) -> bool:
    """
    Returns True if a model matches any wildcard pattern in a list.

    eg.
    - model=`bedrock/us.amazon.nova-micro-v1:0`, allowed_models=`bedrock/*` returns True
    - model=`bedrock/us.amazon.nova-micro-v1:0`, allowed_models=`bedrock/us.*` returns True
    - model=`bedrockzzzz/us.amazon.nova-micro-v1:0`, allowed_models=`bedrock/*` returns False
    """

    if any(
        _is_wildcard_pattern(allowed_model_pattern)
        and is_model_allowed_by_pattern(
            model=model, allowed_model_pattern=allowed_model_pattern
        )
        for allowed_model_pattern in allowed_model_list
    ):
        return True

    if any(
        _is_wildcard_pattern(allowed_model_pattern)
        and _model_custom_llm_provider_matches_wildcard_pattern(
            model=model, allowed_model_pattern=allowed_model_pattern
        )
        for allowed_model_pattern in allowed_model_list
    ):
        return True

    return False

