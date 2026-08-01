
def compute_urgency(time_elapsed: float, time_limit: float) -> float:
    if time_limit <= 0:
        return 1.0
    return min(1.0, max(0.0, time_elapsed / time_limit))


def compute_urgency(time_elapsed: float, time_limit: float) -> float:
    if time_limit <= 0:
        return 1.0
    return min(1.0, max(0.0, time_elapsed / time_limit))

