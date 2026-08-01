
def unshard_tensor_dim(
    placements: Sequence[Placement], dim: int
) -> tuple[Placement, ...]:
    """Disallow the given tensor dimension to be sharded."""
    return tuple(
        p if (not _is_shard_like(p) or p.dim != dim) else Replicate()
        for p in placements
    )

