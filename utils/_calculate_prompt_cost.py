
def _calculate_prompt_cost(
    breakdown: TokenBreakdown,
    model_info: ModelInfo,
    tiered_pricing: Optional[List[dict]],
) -> float:
    """Calculate total prompt cost including cached tokens."""
    if tiered_pricing:
        text_cost = _calculate_tiered_cost(
            tokens=breakdown.text_tokens,
            tiered_pricing=tiered_pricing,
            cost_key="input_cost_per_token",
        )
        cache_cost = _calculate_tiered_cost(
            tokens=breakdown.cached_tokens,
            tiered_pricing=tiered_pricing,
            cost_key="cache_read_input_token_cost",
            fallback_cost_key="input_cost_per_token",
        )
        return text_cost + cache_cost

    input_cost = float(model_info.get("input_cost_per_token") or 0.0)

    # For cache_cost, first try the specific key, then fall back to input_cost.
    cache_cost_val = model_info.get("cache_read_input_token_cost")
    if cache_cost_val is None:
        cache_cost = input_cost
    else:
        cache_cost = float(cache_cost_val)

    return (breakdown.text_tokens * input_cost) + (breakdown.cached_tokens * cache_cost)

