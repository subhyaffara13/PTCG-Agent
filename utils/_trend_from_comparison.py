
def _trend_from_comparison(current_fail: float, previous_fail: float) -> str:
    if previous_fail <= 0:
        return "stable"
    diff = current_fail - previous_fail
    if diff > 0.5:
        return "up"
    if diff < -0.5:
        return "down"
    return "stable"

