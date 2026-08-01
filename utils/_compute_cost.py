
def _compute_cost(cache):
    counts = count_cached_ops(cache)
    return counts["einsum"] + counts["tensordot"]

