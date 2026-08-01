
def parse_get_unified(response, **kwargs):
    """Unified parser for TS.GET. Returns ``[int, float]``."""
    if not response:
        return None
    return [int(response[0]), float(response[1])]

