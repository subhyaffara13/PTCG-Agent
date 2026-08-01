
def get_billable_input_tokens(usage: Usage) -> int:
    """
    Returns the number of billable input tokens.
    Subtracts cached tokens from prompt tokens if applicable.
    """
    details = _parse_prompt_tokens_details(usage)
    return usage.prompt_tokens - details["cache_hit_tokens"]

