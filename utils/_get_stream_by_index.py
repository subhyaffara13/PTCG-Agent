
def _get_stream_by_index(index: int) -> torch.Stream:
    stream = get_external_object_by_index(index)
    assert isinstance(stream, torch.Stream), (
        f"Fork/join stream expected a stream object at index {index}"
    )
    return stream

