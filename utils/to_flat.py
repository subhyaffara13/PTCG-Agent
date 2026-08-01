
def to_flat(coord):
    """Converts from a Minigo coordinate to a flattened coordinate."""
    if coord is None:
        return go_base.N * go_base.N
    return go_base.N * coord[0] + coord[1]

