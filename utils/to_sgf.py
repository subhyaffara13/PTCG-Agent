
def to_sgf(coord):
    """Converts from a Minigo coordinate to an SGF coordinate."""
    if coord is None:
        return ""
    return _SGF_COLUMNS[coord[1]] + _SGF_COLUMNS[coord[0]]

