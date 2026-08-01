
def from_mime_key(d):
    """convert dict with mime-type keys to v3 aliases"""
    d2 = {}
    for alias, mime in _mime_map.items():
        if mime in d:
            d2[alias] = d[mime]
    return d2

