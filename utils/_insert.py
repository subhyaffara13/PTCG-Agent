
def _insert(xval, t, c, k, periodic=False):
    """Insert a single knot at `xval`."""
    #
    # This is a port of the FORTRAN `insert` routine by P. Dierckx,
    # https://github.com/scipy/scipy/blob/maintenance/1.11.x/scipy/interpolate/fitpack/insert.f
    # which carries the following comment:
    #
    # subroutine insert inserts a new knot x into a spline function s(x)
    # of degree k and calculates the b-spline representation of s(x) with
    # respect to the new set of knots. in addition, if iopt.ne.0, s(x)
    # will be considered as a periodic spline with period per=t(n-k)-t(k+1)
    # satisfying the boundary constraints
    #      t(i+n-2*k-1) = t(i)+per  ,i=1,2,...,2*k+1
    #      c(i+n-2*k-1) = c(i)      ,i=1,2,...,k
    # in that case, the knots and b-spline coefficients returned will also
    # satisfy these boundary constraints, i.e.
    #      tt(i+nn-2*k-1) = tt(i)+per  ,i=1,2,...,2*k+1
    #      cc(i+nn-2*k-1) = cc(i)      ,i=1,2,...,k
    interval = _dierckx.find_interval(t, k, float(xval), k, False)
    if interval < 0:
        # extrapolated values are guarded for in BSpline.insert_knot
        raise ValueError(f"Cannot insert the knot at {xval}.")

    # super edge case: a knot with multiplicity > k+1
    # see https://github.com/scipy/scipy/commit/037204c3e91
    if t[interval] == t[interval + k + 1]:
        interval -= 1

    if periodic:
        if (interval + 1 <= 2*k) and (interval + 1 >= t.shape[0] - 2*k):
            # in case of a periodic spline (iopt.ne.0) there must be
            # either at least k interior knots t(j) satisfying t(k+1)<t(j)<=x
            # or at least k interior knots t(j) satisfying x<=t(j)<t(n-k)
            raise ValueError("Not enough internal knots.")

    # knots
    tt = np.r_[t[:interval+1], xval, t[interval+1:]]

    newshape = (c.shape[0] + 1,) + c.shape[1:]
    cc = np.zeros(newshape, dtype=c.dtype)

    # coefficients
    cc[interval+1:, ...] = c[interval:, ...]

    for i in range(interval, interval-k, -1):
        fac = (xval - tt[i]) / (tt[i+k+1] - tt[i])
        cc[i, ...] = fac*c[i, ...] + (1. - fac)*c[i-1, ...]

    cc[:interval - k+1, ...] = c[:interval - k+1, ...]

    if periodic:
        # c   incorporate the boundary conditions for a periodic spline.
        n = tt.shape[0]
        nk = n - k - 1
        n2k = n - 2*k - 1
        T = tt[nk] - tt[k]   # period

        if interval >= nk - k:
            # adjust the left-hand boundary knots & coefs
            tt[:k] = tt[nk - k:nk] - T
            cc[:k, ...] = cc[n2k:n2k + k, ...]

        if interval <= 2*k-1:
            # adjust the right-hand boundary knots & coefs
            tt[n-k:] = tt[k+1:k+1+k] + T
            cc[n2k:n2k + k, ...] = cc[:k, ...]

    return tt, cc

