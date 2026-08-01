
def pick_best(
    cells: Dict[str, BanditCell],
    model_costs: Dict[str, float],
    quality_weight: float = DEFAULT_QUALITY_WEIGHT,
    cost_weight: float = DEFAULT_COST_WEIGHT,
    rng: Optional[random.Random] = None,
) -> str:
    """
    Sample once per model, score each, return the model with highest score.

    cells: {model_name: BanditCell}
    model_costs: {model_name: $/1k tokens}
    """
    if not cells:
        raise ValueError("pick_best called with no models")
    all_costs = list(model_costs.values())
    best_model: Optional[str] = None
    best_score = float("-inf")
    for model, cell in cells.items():
        q = thompson_sample(cell, rng=rng)
        s = score(q, model_costs[model], all_costs, quality_weight, cost_weight)
        if s > best_score:
            best_score = s
            best_model = model
    assert best_model is not None
    return best_model

