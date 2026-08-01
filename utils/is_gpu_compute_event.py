
def is_gpu_compute_event(event: dict[str, Any]) -> bool:
    global gpu_pids
    return (
        "pid" in event
        and event["pid"] in gpu_pids
        and "ph" in event
        and event["ph"] == "X"
    )

