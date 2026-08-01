
def classify_time(time_elapsed: float, time_limit: float) -> tuple[str, str]:
    if time_elapsed > time_limit - 30.0:
        return "FORCE_PASS", "critical"
    if time_elapsed > time_limit - 60.0:
        return "FAST_MOVE", "urgent"
    return "NORMAL", "standard"


def classify_time(time_elapsed: float, time_limit: float) -> tuple[str, str]:
    if time_elapsed > time_limit - 30.0:
        return "FORCE_PASS", "critical"
    if time_elapsed > time_limit - 60.0:
        return "FAST_MOVE", "urgent"
    return "NORMAL", "standard"

