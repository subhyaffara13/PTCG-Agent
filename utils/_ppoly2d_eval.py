
def _ppoly2d_eval(c, xs, xnew, ynew, nu=None):
    """
    Straightforward evaluation of 2-D piecewise polynomial
    """
    if nu is None:
        nu = (0, 0)

    out = np.empty((len(xnew),), dtype=c.dtype)

    nx, ny = c.shape[:2]

    for jout, (x, y) in enumerate(zip(xnew, ynew)):
        if not ((xs[0][0] <= x <= xs[0][-1]) and
                (xs[1][0] <= y <= xs[1][-1])):
            out[jout] = np.nan
            continue

        j1 = np.searchsorted(xs[0], x) - 1
        j2 = np.searchsorted(xs[1], y) - 1

        s1 = x - xs[0][j1]
        s2 = y - xs[1][j2]

        val = 0

        for k1 in range(c.shape[0]):
            for k2 in range(c.shape[1]):
                val += (c[nx-k1-1,ny-k2-1,j1,j2]
                        * _dpow(s1, k1, nu[0])
                        * _dpow(s2, k2, nu[1]))

        out[jout] = val

    return out

