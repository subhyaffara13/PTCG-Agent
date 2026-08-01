
def _flatten_resp3_state_pairs(state):
    """Yield key/value pairs from a RESP3 sentinel-state map as a flat
    iterable suitable for ``parse_sentinel_state``.
    """
    for key, value in state.items():
        yield key
        yield value

