
def _extract_token_breakdown(usage: Usage) -> TokenBreakdown:
    """Extract token counts from usage, handling cached and reasoning tokens."""
    cached_tokens = 0
    if usage.prompt_tokens_details and hasattr(
        usage.prompt_tokens_details, "cached_tokens"
    ):
        cached_tokens = usage.prompt_tokens_details.cached_tokens or 0

    text_tokens = usage.prompt_tokens - cached_tokens

    reasoning_tokens = 0
    if (
        hasattr(usage, "completion_tokens_details")
        and usage.completion_tokens_details
        and hasattr(usage.completion_tokens_details, "reasoning_tokens")
    ):
        reasoning_tokens = usage.completion_tokens_details.reasoning_tokens or 0

    completion_tokens = (usage.completion_tokens or 0) - reasoning_tokens

    return TokenBreakdown(
        text_tokens, cached_tokens, completion_tokens, reasoning_tokens
    )

