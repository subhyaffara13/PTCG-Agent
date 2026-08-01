
def _rec_strip(g, v):
    """Recursive helper for :func:`_rec_strip`."""
    if not v:
        return dup_strip(g)

    w = v - 1

    return dmp_strip([ _rec_strip(c, w) for c in g ], v)

