
def _make_peekable(stream):
    """return stream as an object with a peek() method"""
    import io
    if hasattr(stream, 'peek'):
        return stream
    if not (hasattr(stream, 'tell') and hasattr(stream, 'seek')):
        try:
            return io.BufferedReader(stream)
        except Exception:
            pass
    return _PeekableReader(stream)

