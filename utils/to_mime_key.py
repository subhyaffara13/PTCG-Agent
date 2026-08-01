
def to_mime_key(d):
    """convert dict with v3 aliases to plain mime-type keys"""
    for alias, mime in _mime_map.items():
        if alias in d:
            d[mime] = d.pop(alias)
    return d

