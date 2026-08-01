
def _extract_cache_read_input_tokens(usage_obj) -> int:
    """
    Extract cache_read_input_tokens from usage object.

    Checks both:
    1. Top-level cache_read_input_tokens (Anthropic format)
    2. prompt_tokens_details.cached_tokens (Gemini, OpenAI format)

    See: https://github.com/BerriAI/litellm/issues/18520

    Args:
        usage_obj: Usage object from LLM response

    Returns:
        int: Number of cached tokens read, defaults to 0
    """
    cache_read_input_tokens = usage_obj.get("cache_read_input_tokens") or 0

    # Check prompt_tokens_details.cached_tokens (used by Gemini and other providers)
    if hasattr(usage_obj, "prompt_tokens_details"):
        prompt_tokens_details = getattr(usage_obj, "prompt_tokens_details", None)
        if prompt_tokens_details is not None and hasattr(
            prompt_tokens_details, "cached_tokens"
        ):
            cached_tokens = getattr(prompt_tokens_details, "cached_tokens", None)
            if (
                cached_tokens is not None
                and isinstance(cached_tokens, (int, float))
                and cached_tokens > 0
            ):
                cache_read_input_tokens = cached_tokens

    return cache_read_input_tokens

