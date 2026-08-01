
def from_flat(flat):
    """Converts from a flattened coordinate to a Minigo coordinate."""
    if flat == go_base.N * go_base.N:
        return None
    return divmod(flat, go_base.N)

