
def _replicate_dims_start_at(
    placements: Sequence[Placement], start_dim: int = 0
) -> tuple[Placement, ...]:
    new_placements: list[Placement] = []
    for p in placements:
        if p.is_partial() or (_is_shard_like(p) and p.dim >= start_dim):
            new_placements.append(Replicate())  # make it replicate
        else:
            new_placements.append(p)  # keep the placement
    return tuple(new_placements)

