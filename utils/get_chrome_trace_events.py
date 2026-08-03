import json
from typing import Any

def get_chrome_trace_events(filename: str) -> list[dict[str, Any]]:
    with open(filename) as f:
        data = json.load(f)
    events = data["traceEvents"]
    return events

