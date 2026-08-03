from typing import Tuple
import math


def calculate_baseline_stats(history: list) -> Tuple[float, float]:
    if not history:
        return 0.5, 0.5
    mean = sum(history) / len(history)
    if len(history) < 2:
        return mean, 0.5
    variance = sum((x - mean) ** 2 for x in history) / (len(history) - 1)
    stddev = max(0.01, math.sqrt(variance))
    return mean, stddev

