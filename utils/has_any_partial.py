
def has_any_partial(
    input_placements: tuple[Placement, ...],
    output_placements: tuple[Placement, ...],
) -> bool:
    """Check if any placement is Partial (any reduce op)."""
    for p in (*input_placements, *output_placements):
        if isinstance(p, Partial):
            return True
    return False

