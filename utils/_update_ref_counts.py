
def _update_ref_counts(
    dim_to_keys: Dict[str, Set[ArrayIndexType]],
    dim_ref_counts: Dict[int, Set[str]],
    dims: ArrayIndexType,
) -> None:
    for dim in dims:
        count = len(dim_to_keys[dim])
        if count <= 1:
            dim_ref_counts[2].discard(dim)
            dim_ref_counts[3].discard(dim)
        elif count == 2:
            dim_ref_counts[2].add(dim)
            dim_ref_counts[3].discard(dim)
        else:
            dim_ref_counts[2].add(dim)
            dim_ref_counts[3].add(dim)

