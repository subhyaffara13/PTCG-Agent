
def _normalize_placements_for_grad(
    placements: tuple[Placement, ...],
) -> tuple[Placement, ...]:
    """
    Normalize gradient placements by converting Partial to Replicate.

    See the gradient placement guarantees documented in DTensor.from_local's docstring
    for why Partial forward placements map to Replicate gradient placements. We do this
    for both from_local and to_local backward.
    """
    normalized: list[Placement] = []
    for p in placements:
        if p.is_partial():
            normalized.append(Replicate())
        else:
            normalized.append(p)
    return tuple(normalized)

