
def _get_candidate(
    output: ArrayIndexType,
    sizes: Dict[str, int],
    remaining: Dict[ArrayIndexType, int],
    footprints: Dict[ArrayIndexType, int],
    dim_ref_counts: Dict[int, Set[str]],
    k1: ArrayIndexType,
    k2: ArrayIndexType,
    cost_fn: Any,
) -> GreedyContractionType:
    either = k1 | k2
    two = k1 & k2
    one = either - two
    k12 = (either & output) | (two & dim_ref_counts[3]) | (one & dim_ref_counts[2])
    cost = cost_fn(
        compute_size_by_dict(k12, sizes),
        footprints[k1],
        footprints[k2],
        k12,
        k1,
        k2,
    )
    id1 = remaining[k1]
    id2 = remaining[k2]
    if id1 > id2:
        k1, id1, k2, id2 = k2, id2, k1, id1
    cost = cost, id2, id1  # break ties to ensure determinism
    return cost, k1, k2, k12

