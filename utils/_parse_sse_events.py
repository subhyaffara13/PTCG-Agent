
def _parse_sse_events(raw: bytes) -> List[tuple]:
    """Return a list of (event_type, parsed_data_dict) from raw SSE bytes."""
    text = raw.decode("utf-8", errors="replace")
    lines = text.split("\n")
    events: List[tuple] = []
    current_event_type: Optional[str] = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("event:"):
            current_event_type = stripped[len("event:") :].strip()
            continue
        if not stripped.startswith("data:"):
            continue
        data_str = stripped[len("data:") :].strip()
        try:
            data = json.loads(data_str)
        except (json.JSONDecodeError, ValueError):
            continue
        event_type = current_event_type or data.get("type", "")
        current_event_type = None
        events.append((event_type, data))
    return events

