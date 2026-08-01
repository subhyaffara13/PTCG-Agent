
def _get_event_by_index(index: int) -> torch.Event:
    event = get_external_object_by_index(index)
    assert isinstance(event, torch.Event), (
        f"Record/wait event expected an event object at index {index}"
    )
    return event

