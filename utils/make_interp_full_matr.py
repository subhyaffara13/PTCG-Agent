
def make_interp_full_matr(x, y, t, k):
    """Assemble an spline order k with knots t to interpolate
    y(x) using full matrices.
    Not-a-knot BC only.

    This routine is here for testing only (even though it's functional).
    """
    assert x.size == y.size
    assert t.size == x.size + k + 1
    n = x.size

    A = np.zeros((n, n), dtype=np.float64)

    for j in range(n):
        xval = x[j]
        if xval == t[k]:
            left = k
        else:
            left = np.searchsorted(t, xval) - 1

        # fill a row
        bb = _dierckx.evaluate_all_bspl(t, k, xval, left)
        A[j, left-k:left+1] = bb

    c = sl.solve(A, y)
    return c

