
def _cost_per_token_custom_pricing_helper(
    prompt_tokens: float = 0,
    completion_tokens: float = 0,
    response_time_ms: Optional[float] = 0.0,
    cached_tokens: float = 0,
    cache_creation_tokens: float = 0,
    ### CUSTOM PRICING ###
    custom_cost_per_token: Optional[CostPerToken] = None,
    custom_cost_per_second: Optional[float] = None,
) -> Optional[Tuple[float, float]]:
    """Internal helper function for calculating cost, if custom pricing given.

    prompt_tokens is assumed to include both cached_tokens and cache_creation_tokens
    (OpenAI-compatible convention). Anthropic-style usage where prompt_tokens excludes
    cache tokens is handled at the caller (cost_per_token) before invoking this helper.
    """
    if custom_cost_per_token is None and custom_cost_per_second is None:
        return None

    if custom_cost_per_token is not None:
        input_cost_per_token = custom_cost_per_token["input_cost_per_token"]
        output_cost_per_token = custom_cost_per_token["output_cost_per_token"]

        cache_read_input_token_cost = custom_cost_per_token.get(
            "cache_read_input_token_cost",
            input_cost_per_token,
        )
        cache_creation_input_token_cost = custom_cost_per_token.get(
            "cache_creation_input_token_cost",
            input_cost_per_token,
        )

        regular_prompt_tokens = max(
            prompt_tokens - cached_tokens - cache_creation_tokens,
            0,
        )

        input_cost = (
            regular_prompt_tokens * input_cost_per_token
            + cached_tokens * cache_read_input_token_cost
            + cache_creation_tokens * cache_creation_input_token_cost
        )
        output_cost = completion_tokens * output_cost_per_token
        return input_cost, output_cost
    elif custom_cost_per_second is not None:
        output_cost = custom_cost_per_second * response_time_ms / 1000  # type: ignore
        return 0, output_cost

    return None

