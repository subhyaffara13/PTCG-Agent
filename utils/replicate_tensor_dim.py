
def replicate_tensor_dim(
    placements: Sequence[Placement], dim: int
) -> tuple[Placement, ...]:
    """Force the given tensor dimension to be replicated."""
    return tuple(
        Replicate() if p.is_partial() or (_is_shard_like(p) and p.dim == dim) else p
        for p in placements
    )

