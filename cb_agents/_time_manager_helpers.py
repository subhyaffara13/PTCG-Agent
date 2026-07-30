import datetime
from typing import Any

def classify_time(time_elapsed: float, time_limit: float) -> tuple[str, str]:
    if time_elapsed > time_limit - 30.0:
        return "FORCE_PASS", "critical"
    if time_elapsed > time_limit - 60.0:
        return "FAST_MOVE", "urgent"
    return "NORMAL", "standard"

def compute_urgency(time_elapsed: float, time_limit: float) -> float:
    if time_limit <= 0:
        return 1.0
    return min(1.0, max(0.0, time_elapsed / time_limit))

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

def build_log_entry(packet, result, time_limit: float = 600.0):
    time_el = packet.get("time_elapsed")
    directive_val = result.get("directive") if isinstance(result, dict) else result
    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent":     "TimeManager",
        "input":     packet,
        "reasoning": {
            "threshold_fast":       time_limit - 60.0,
            "threshold_force_pass": time_limit - 30.0,
            "evaluation": f"time_elapsed={time_el} -> directive={directive_val}",
        },
        "output": result,
    }
