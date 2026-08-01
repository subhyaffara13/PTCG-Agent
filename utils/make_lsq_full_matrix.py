
def make_lsq_full_matrix(x, y, t, k=3):
    """Make the least-square spline, full matrices."""
    x, y, t = map(np.asarray, (x, y, t))
    m = x.size
    n = t.size - k - 1

    A = np.zeros((m, n), dtype=np.float64)

    for j in range(m):
        xval = x[j]
        # find interval
        if xval == t[k]:
            left = k
        else:
            left = np.searchsorted(t, xval) - 1

        # fill a row
        bb = _dierckx.evaluate_all_bspl(t, k, xval, left)
        A[j, left-k:left+1] = bb

    # have observation matrix, can solve the LSQ problem
    B = np.dot(A.T, A)
    Y = np.dot(A.T, y)
    c = sl.solve(B, Y)

    return c, (A, Y)

