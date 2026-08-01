
def get_sorted_gpu_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sorted_gpu_events: list[dict[str, Any]] = []
    for event in events:
        if not is_gpu_compute_event(event):
            continue
        sorted_gpu_events.append(event)
    return sorted(sorted_gpu_events, key=operator.itemgetter("ts"))

