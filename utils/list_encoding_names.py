
def list_encoding_names() -> list[str]:
    with _lock:
        if ENCODING_CONSTRUCTORS is None:
            _find_constructors()
            assert ENCODING_CONSTRUCTORS is not None
        return list(ENCODING_CONSTRUCTORS)

