
def _extract_cache_creation_tokens(usage_obj: dict) -> int:
    """
    Anthropic: top-level cache_creation_input_tokens field.
    OpenAI-compatible (kimi-k2 etc.): prompt_tokens_details.cache_write_tokens
    or prompt_tokens_details.cache_creation_tokens.
    """
    explicit = usage_obj.get("cache_creation_input_tokens", 0) or 0
    if explicit:
        return int(explicit)
    details = usage_obj.get("prompt_tokens_details") or {}
    return int(
        details.get("cache_write_tokens", 0)
        or details.get("cache_creation_tokens", 0)
        or 0
    )

