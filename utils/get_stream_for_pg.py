
def get_stream_for_pg(pg_key: str) -> int:
    """Return a unique stream ID for the given process group key."""
    global _stream_id_counter
    if pg_key not in _stream_id_map:
        _stream_id_map[pg_key] = _stream_id_counter  # type: ignore[assignment]
        _stream_id_counter += 1
    return _stream_id_map[pg_key]  # type: ignore[return-value]

