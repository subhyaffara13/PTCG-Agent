
def synchronize_stream(stream_index: int) -> None:
    stream = _get_stream_by_index(stream_index)
    stream.synchronize()

