
def _split_events_by_invocation(
    events: list[dict[str, Any]],
    gap_threshold_ns: float = 1000.0,
) -> list[list[dict[str, Any]]]:
    """Split events into separate invocations based on time gaps."""
    if not events:
        return []

    events_sorted = sorted(events, key=lambda e: e.get("ts", 0))
    invocations: list[list[dict[str, Any]]] = [[]]
    prev_end = events_sorted[0].get("ts", 0)

    for event in events_sorted:
        ts = event.get("ts", 0)
        dur = event.get("dur", 0)
        if ts - prev_end > gap_threshold_ns and invocations[-1]:
            invocations.append([])
        invocations[-1].append(event)
        prev_end = max(prev_end, ts + dur)

    return [inv for inv in invocations if inv]

