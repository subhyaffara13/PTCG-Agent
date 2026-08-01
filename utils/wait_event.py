
def wait_event(event_index: int, stream_index: int) -> None:
    event = _get_event_by_index(event_index)
    stream = _get_stream_by_index(stream_index)
    event.wait(stream)

