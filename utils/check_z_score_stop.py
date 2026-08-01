
def check_z_score_stop(branch_results: list, baseline_history: list, min_games: int, z_threshold: float) -> Tuple[bool, float, float, float]:
    if len(branch_results) < min_games:
        return False, 0.0, 0.0, 0.0
    branch_mean = sum(branch_results) / len(branch_results)
    baseline_mean, baseline_std = calculate_baseline_stats(baseline_history)
    z_score = (branch_mean - baseline_mean) / (baseline_std / math.sqrt(len(branch_results)))
    return z_score < -z_threshold, z_score, branch_mean, baseline_mean

