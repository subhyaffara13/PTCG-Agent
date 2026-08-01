
def _sum_abs_delta_rank(
    ranks_a: dict[str, int],
    ranks_b: dict[str, int],
) -> int:
    return sum(abs(ranks_a[m] - ranks_b[m]) for m in ranks_a if m in ranks_b)

