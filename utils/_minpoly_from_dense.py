
def _minpoly_from_dense(minpoly, ring):
    r"""
    Change representation of the minimal polynomial from ``DMP`` to
    ``PolyElement`` for a given ring.
    """
    minpoly_ = ring.zero

    for monom, coeff in minpoly.terms():
        minpoly_[monom] = ring.domain(coeff)

    return minpoly_

