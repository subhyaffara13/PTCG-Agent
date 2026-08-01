
def _skip_dim(
    placements: tuple[Placement, ...], skipped_dim: int
) -> tuple[Placement, ...]:
    new_placements: list[Placement] = []
    for p in placements:
        if isinstance(p, _StridedShard) and p.dim >= skipped_dim:
            new_placements.append(_StridedShard(p.dim - 1, split_factor=p.split_factor))
        elif isinstance(p, Shard) and p.dim >= skipped_dim:
            new_placements.append(Shard(p.dim - 1))
        else:
            new_placements.append(p)
    return tuple(new_placements)

