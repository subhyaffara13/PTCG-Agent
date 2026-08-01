
def _pass_through_partials(
    num_inputs: int = 1,
) -> list[list[Placement | _ShardingPlaceholder]]:
    """Pass-through strategies for all supported reduce ops."""
    return [[Partial(op)] * (1 + num_inputs) for op in ("sum", "avg", "max", "min")]

