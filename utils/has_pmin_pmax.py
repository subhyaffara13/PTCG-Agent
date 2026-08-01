
def has_pmin_pmax(
    input_placements: tuple[Placement, ...],
    output_placements: tuple[Placement, ...],
) -> bool:
    """Check if any placement is Partial(min) or Partial(max)."""
    for p in (*input_placements, *output_placements):
        if isinstance(p, Partial) and p.reduce_op in ("min", "max"):
            return True
    return False

