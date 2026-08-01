
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

