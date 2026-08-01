
def _compute_cache_only_cost(
    model_info: "ModelInfo", usage: "Usage", service_tier: str | None = None
) -> float:
    """
    Return only the cache-related portion of the prompt cost (cache read + cache write).

    These costs must NOT be scaled by geo/speed multipliers because the old
    explicit ``fast/`` model entries carried unchanged cache rates while
    multiplying only the regular input/output token costs.
    """
    if usage.prompt_tokens_details is None:
        return 0.0

    prompt_tokens_details = _parse_prompt_tokens_details(usage)
    (
        _,
        _,
        cache_creation_cost,
        cache_creation_cost_above_1hr,
        cache_read_cost,
    ) = _get_token_base_cost(
        model_info=model_info, usage=usage, service_tier=service_tier
    )

    cache_cost = float(prompt_tokens_details["cache_hit_tokens"]) * cache_read_cost

    if (
        prompt_tokens_details["cache_creation_tokens"]
        or prompt_tokens_details["cache_creation_token_details"] is not None
    ):
        cache_cost += calculate_cache_writing_cost(
            cache_creation_tokens=prompt_tokens_details["cache_creation_tokens"],
            cache_creation_token_details=prompt_tokens_details[
                "cache_creation_token_details"
            ],
            cache_creation_cost_above_1hr=cache_creation_cost_above_1hr,
            cache_creation_cost=cache_creation_cost,
        )

    return cache_cost

