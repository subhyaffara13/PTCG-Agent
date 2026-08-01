
def normalized_cost(model_cost: float, all_costs: List[float]) -> float:
    """
    Map a raw $/1k-token cost into [0, 1] where 0 = most expensive, 1 = cheapest.
    Returns 0.5 when there's no spread.
    """
    if not all_costs:
        return 0.5
    lo, hi = min(all_costs), max(all_costs)
    if hi == lo:
        return 0.5
    return 1.0 - ((model_cost - lo) / (hi - lo))

