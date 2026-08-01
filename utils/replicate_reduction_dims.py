
def replicate_reduction_dims(
    placements: tuple[Placement, ...], reduction_dims: list[int]
) -> tuple[Placement, ...]:
    # replicate the reduction dims if not reduction_linear
    new_placements: list[Placement] = []

    for p in placements:
        if p.is_partial():
            new_placements.append(Replicate())
        elif _is_shard_like(p) and p.dim in reduction_dims:
            new_placements.append(Replicate())
        else:
            new_placements.append(p)

    return tuple(new_placements)

