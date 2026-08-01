
def _calculate_completion_cost(
    breakdown: TokenBreakdown,
    model_info: ModelInfo,
    tiered_pricing: Optional[List[dict]],
) -> float:
    """Calculate total completion cost including reasoning tokens."""
    if tiered_pricing:
        completion_cost = _calculate_tiered_cost(
            tokens=breakdown.completion_tokens,
            tiered_pricing=tiered_pricing,
            cost_key="output_cost_per_token",
        )
        reasoning_cost = _calculate_tiered_cost(
            tokens=breakdown.reasoning_tokens,
            tiered_pricing=tiered_pricing,
            cost_key="output_cost_per_reasoning_token",
            fallback_cost_key="output_cost_per_token",
        )
        return completion_cost + reasoning_cost

    output_cost = float(model_info.get("output_cost_per_token") or 0.0)

    # For reasoning_cost, first try the specific key, then fall back to output_cost.
    reasoning_cost_val = model_info.get("output_cost_per_reasoning_token")
    if reasoning_cost_val is None:
        reasoning_cost = output_cost
    else:
        reasoning_cost = float(reasoning_cost_val)

    return (breakdown.completion_tokens * output_cost) + (
        breakdown.reasoning_tokens * reasoning_cost
    )

