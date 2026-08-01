
def wait_stream(waiting_stream_index: int, waited_on_stream_index: int) -> None:
    waiting = _get_stream_by_index(waiting_stream_index)
    waited_on = _get_stream_by_index(waited_on_stream_index)
    waiting.wait_stream(waited_on)

