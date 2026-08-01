
def to_gtp(coord):
    """Converts from a Minigo coordinate to a GTP coordinate."""
    if coord is None:
        return "pass"
    y, x = coord
    return f"{_GTP_COLUMNS[x]}{go_base.N - y}"

