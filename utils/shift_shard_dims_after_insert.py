
def shift_shard_dims_after_insert(
    placements: Sequence[Placement], insert_dim: int = 0
) -> Sequence[Placement]:
    normalized_placements: list[Placement] = []
    for placement in placements:
        if isinstance(placement, _StridedShard) and placement.dim >= insert_dim:
            normalized_placements.append(
                _StridedShard(placement.dim + 1, split_factor=placement.split_factor)
            )
        elif isinstance(placement, Shard) and placement.dim >= insert_dim:
            normalized_placements.append(Shard(placement.dim + 1))
        else:
            normalized_placements.append(placement)
    return normalized_placements

