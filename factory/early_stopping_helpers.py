import math
from typing import Tuple

def calculate_baseline_stats(history: list) -> Tuple[float, float]:
    if not history:
        return 0.5, 0.5
    mean = sum(history) / len(history)
    if len(history) < 2:
        return mean, 0.5
    variance = sum((x - mean) ** 2 for x in history) / (len(history) - 1)
    stddev = max(0.01, math.sqrt(variance))
    return mean, stddev

def check_z_score_stop(branch_results: list, baseline_history: list, min_games: int, z_threshold: float) -> Tuple[bool, float, float, float]:
    if len(branch_results) < min_games:
        return False, 0.0, 0.0, 0.0
    branch_mean = sum(branch_results) / len(branch_results)
    baseline_mean, baseline_std = calculate_baseline_stats(baseline_history)
    z_score = (branch_mean - baseline_mean) / (baseline_std / math.sqrt(len(branch_results)))
    return z_score < -z_threshold, z_score, branch_mean, baseline_mean
