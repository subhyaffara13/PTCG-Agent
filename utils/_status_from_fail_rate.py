
def _status_from_fail_rate(fail_rate: float) -> str:
    if fail_rate > 15:
        return "critical"
    if fail_rate > 5:
        return "warning"
    return "healthy"

