
def disc(t, k):
    """Discontinuity matrix: jumps of k-th derivatives of b-splines at internal knots.

    See Eqs. (9)-(10) of Ref. [1], or, equivalently, Eq. (3.43) of Ref. [2].

    This routine assumes internal knots are all simple (have multiplicity =1).

    Parameters
    ----------
    t : ndarray, 1D, shape(n,)
        Knots.
    k : int
        The spline degree

    Returns
    -------
    disc : ndarray, shape(n-2*k-1, k+2)
        The jumps of the k-th derivatives of b-splines at internal knots,
        ``t[k+1], ...., t[n-k-1]``.
    offset : ndarray, shape(2-2*k-1,)
        Offsets
    nc : int

    Notes
    -----

    The normalization here follows FITPACK:
    (https://github.com/scipy/scipy/blob/maintenance/1.11.x/scipy/interpolate/fitpack/fpdisc.f#L36)

    The k-th derivative jumps are multiplied by a factor::

        (delta / nrint)**k / k!

    where ``delta`` is the length of the interval spanned by internal knots, and
    ``nrint`` is one less the number of internal knots (i.e., the number of
    subintervals between them).

    References
    ----------
    .. [1] Paul Dierckx, Algorithms for smoothing data with periodic and parametric
           splines, Computer Graphics and Image Processing, vol. 20, p. 171 (1982).
           :doi:`10.1016/0146-664X(82)90043-0`

    .. [2] Tom Lyche and Knut Morken, Spline methods,
        https://web.archive.org/web/20221205112612/https://www.uio.no/studier/emner/matnat/ifi/nedlagte-emner/INF-MAT5340/v05/undervisningsmateriale/hele.pdf

    """
    n = t.shape[0]

    # the length of the base interval spanned by internal knots & the number
    # of subintervas between these internal knots
    delta = t[n - k - 1] - t[k]
    nrint = n - 2*k - 1

    matr = np.empty((nrint - 1, k + 2), dtype=float)
    for jj in range(nrint - 1):
        j = jj + k + 1
        for ii in range(k + 2):
            i = jj + ii
            matr[jj, ii] = (t[i + k + 1] - t[i]) / prodd(t, i, j, k)
        # NB: equivalent to
        # row = [(t[i + k + 1] - t[i]) / prodd(t, i, j, k) for i in range(j-k-1, j+1)]
        # assert (matr[j-k-1, :] == row).all()

    # follow FITPACK
    matr *= (delta/ nrint)**k

    # make it packed
    offset = np.array([i for i in range(nrint-1)], dtype=np.int64)
    nc = n - k - 1
    return matr, offset, nc

