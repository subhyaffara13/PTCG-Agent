
def _observed_delta(
    baseline_pairs: dict[tuple, dict[str, float]],
    variant_pairs: dict[tuple, dict[str, float]],
    models: list[str],
) -> int:
    lb_baseline = _leaderboard_from_pairs(baseline_pairs.values(), models)
    lb_variant = _leaderboard_from_pairs(variant_pairs.values(), models)
    return _sum_abs_delta_rank(
        _ranks_from_leaderboard(lb_baseline),
        _ranks_from_leaderboard(lb_variant),
    )

