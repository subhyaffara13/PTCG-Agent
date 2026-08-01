
def from_sgf(sgfc):
    """Converts from an SGF coordinate to a Minigo coordinate."""
    if sgfc is None or sgfc == "" or (go_base.N <= 19 and sgfc == "tt"):
        return None
    return _SGF_COLUMNS.index(sgfc[1]), _SGF_COLUMNS.index(sgfc[0])

