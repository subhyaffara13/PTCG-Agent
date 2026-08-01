
def build_tick_result(packet: dict, time_limit: float) -> dict:
    time_elapsed: float = float(packet.get("time_elapsed", 0.0))
    directive, mode     = classify_time(time_elapsed, time_limit)
    urgency             = compute_urgency(time_elapsed, time_limit)
    time_remaining      = max(0.0, time_limit - time_elapsed)
    result: dict[str, Any] = {
        "directive":      directive,
        "mode":           mode,
        "urgency":        round(urgency, 4),
        "time_remaining": round(time_remaining, 2),
    }
    return result


def build_tick_result(packet: dict, time_limit: float) -> dict:
    time_elapsed: float = float(packet.get("time_elapsed", 0.0))
    directive, mode     = classify_time(time_elapsed, time_limit)
    urgency             = compute_urgency(time_elapsed, time_limit)
    time_remaining      = max(0.0, time_limit - time_elapsed)
    result: dict[str, Any] = {
        "directive":      directive,
        "mode":           mode,
        "urgency":        round(urgency, 4),
        "time_remaining": round(time_remaining, 2),
    }
    return result

