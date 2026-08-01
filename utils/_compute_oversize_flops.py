
def _compute_oversize_flops(
    inputs: Tuple[FrozenSet[str]],
    remaining: List[ArrayIndexType],
    output: ArrayIndexType,
    size_dict: Dict[str, int],
) -> int:
    """Compute the flop count for a contraction of all remaining arguments. This
    is used when a memory limit means that no pairwise contractions can be made.
    """
    idx_contraction = frozenset.union(*map(inputs.__getitem__, remaining))  # type: ignore
    inner = idx_contraction - output
    num_terms = len(remaining)
    return flop_count(idx_contraction, bool(inner), num_terms, size_dict)

