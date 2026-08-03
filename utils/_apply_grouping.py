from typing import Any

def _apply_grouping(
    events: list[dict[str, Any]], group_by_sm: bool, per_cta_occupancy: bool
) -> list[dict[str, Any]]:
    """Apply grouping transformation to events."""
    if per_cta_occupancy:
        return _group_events_per_cta_occupancy(events)
    elif group_by_sm:
        return _group_events_by_sm(events)
    return events

