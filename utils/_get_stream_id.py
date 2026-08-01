
def _get_stream_id(stream: torch.cuda.Stream) -> int:
    """Return a small, stable stream ID for the given CUDA stream."""
    global _stream_id_counter
    key = stream.cuda_stream
    if key not in _stream_id_map:
        _stream_id_map[key] = _stream_id_counter
        _stream_id_counter += 1
    return _stream_id_map[key]

