
def _canonicalize_profiler_events(events):
    """
    Extract and format all events with stack traces in a canonical way
    for deterministic testing.
    """
    events_with_traces = []

    for event in events:
        # Extract relevant fields
        event_name = event.get("name", "")
        node_name = event["args"].get("node_name", "")
        stack_trace = event["args"].get("stack_trace", "")

        # Get the last non-empty line of the stack trace
        lines = [s.strip() for s in stack_trace.split("\n") if s.strip()]
        stack_trace = lines[-1] if lines else ""

        events_with_traces.append(
            {
                "event_name": event_name[:30],
                "node_name": node_name,
                "stack_trace": stack_trace,
                "start_time": event.get("ts", 0),
            }
        )

    # Sort by node_name for deterministic ordering
    events_with_traces.sort(key=lambda x: x["start_time"])

    # Format as a string
    lines: list[str] = []
    for evt in events_with_traces:
        lines.append(
            f"event={evt['event_name']} node={evt['node_name']} stack_trace={evt['stack_trace']}"
        )

    return "\n".join(lines)

