
def _make_multiples(b):
    """Increase knot multiplicity."""
    c, k = b.c, b.k

    t1 = b.t.copy()
    t1[17:19] = t1[17]
    t1[22] = t1[21]
    yield BSpline(t1, c, k)

    t1 = b.t.copy()
    t1[:k+1] = t1[0]
    yield BSpline(t1, c, k)

    t1 = b.t.copy()
    t1[-k-1:] = t1[-1]
    yield BSpline(t1, c, k)

