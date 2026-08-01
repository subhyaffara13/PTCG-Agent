
def _extract_cache_read_tokens(usage_obj: dict) -> int:
    """
    Anthropic: top-level cache_read_input_tokens field.
    OpenAI-compatible (moonshotai, openai, deepseek, etc.): prompt_tokens_details.cached_tokens.
    """
    explicit = usage_obj.get("cache_read_input_tokens", 0) or 0
    if explicit:
        return int(explicit)
    details = usage_obj.get("prompt_tokens_details") or {}
    return int(details.get("cached_tokens", 0) or 0)

