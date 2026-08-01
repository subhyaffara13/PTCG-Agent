
def qform(A: Tensor | None, S: Tensor):
    """Return quadratic form :math:`S^T A S`."""
    return bform(S, A, S)

