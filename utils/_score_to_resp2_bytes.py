
def _score_to_resp2_bytes(value):
    """Re-encode a score back to the bytes form Redis returns on the RESP2
    wire so that custom ``score_cast_func`` callables observe the same
    input type they would receive on a RESP2 connection when the wire
    protocol is RESP3 but legacy response shapes are requested.
    """
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode()
    if isinstance(value, bool):
        return b"1" if value else b"0"
    return format(float(value), ".17g").encode()

