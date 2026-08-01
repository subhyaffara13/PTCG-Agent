
def parse_get(response):
    """Parse get response. Used by TS.GET (legacy shape)."""
    if not response:
        return None
    return int(response[0]), float(response[1])

