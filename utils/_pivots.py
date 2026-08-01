
def _pivots(A_rref):
    """Return the pivots from the rref of A."""
    return tuple(sorted(map(min, A_rref.to_sdm().values())))

