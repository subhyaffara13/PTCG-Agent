
def _model_custom_llm_provider_matches_wildcard_pattern(
    model: str, allowed_model_pattern: str
) -> bool:
    """
    Returns True for this scenario:
    - `model=gpt-4o`
    - `allowed_model_pattern=openai/*`

    or
    - `model=claude-3-5-sonnet-20240620`
    - `allowed_model_pattern=anthropic/*`
    """
    try:
        model, custom_llm_provider, _, _ = get_llm_provider(model=model)
    except Exception:
        return False

    return is_model_allowed_by_pattern(
        model=f"{custom_llm_provider}/{model}",
        allowed_model_pattern=allowed_model_pattern,
    )

