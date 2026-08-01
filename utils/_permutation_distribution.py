
def _permutation_distribution(
    baseline_pairs: dict[tuple, dict[str, float]],
    variant_pairs: dict[tuple, dict[str, float]],
    models: list[str],
    n_permutations: int,
    rng: random.Random,
) -> list[int]:
    """Shuffle labels across the pooled pairs, recompute Σ|Δrank| each time.

    Under H0 ("baseline and variant come from the same distribution"),
    the label is arbitrary. The fraction of permutations producing a
    statistic at least as extreme as observed is the p-value.

    Both arms must have the same number of pairs for the permutation to
    be well-defined; we subsample the larger to match the smaller.
    """
    a_ids = list(baseline_pairs.keys())
    b_ids = list(variant_pairs.keys())
    n = min(len(a_ids), len(b_ids))
    if n == 0:
        return []

    # Pool of (pair_id, source-arm) tuples. Each pair_id may appear once
    # per source arm (the two arms are independent draws from
    # comparable matchups, not the literal same pair).
    pool: list[tuple[str, dict[str, float]]] = []
    for pid in a_ids[:n]:
        pool.append(("A", baseline_pairs[pid]))
    for pid in b_ids[:n]:
        pool.append(("B", variant_pairs[pid]))

    dist: list[int] = []
    for _ in range(n_permutations):
        rng.shuffle(pool)
        a_sample = [p[1] for p in pool[:n]]
        b_sample = [p[1] for p in pool[n:2 * n]]
        lb_a = _leaderboard_from_pairs(a_sample, models)
        lb_b = _leaderboard_from_pairs(b_sample, models)
        dist.append(_sum_abs_delta_rank(
            _ranks_from_leaderboard(lb_a),
            _ranks_from_leaderboard(lb_b),
        ))
    return dist

