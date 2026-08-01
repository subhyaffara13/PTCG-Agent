
def synchronize_event(event_index: int) -> None:
    event = _get_event_by_index(event_index)
    event.synchronize()

