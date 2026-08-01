
def _make_periodic_spline(x, y, t, k, axis, *, xp):
    '''
    Compute the (coefficients of) interpolating B-spline with periodic
    boundary conditions.

    Parameters
    ----------
    x : array_like, shape (n,)
        Abscissas.
    y : array_like, shape (n,)
        Ordinates.
    k : int
        B-spline degree.
    t : array_like, shape (n + 2 * k,).
        Knots taken on a circle, ``k`` on the left and ``k`` on the right
        of the vector ``x``.

    Returns
    -------
    b : `BSpline` object
        A `BSpline` object of the degree ``k`` and with knots ``t``.

    Notes
    -----
    The original system is formed by ``n + k - 1`` equations where the first
    ``k - 1`` of them stand for the ``k - 1`` derivatives continuity on the
    edges while the other equations correspond to an interpolating case
    (matching all the input points). Due to a special form of knot vector, it
    can be proved that in the original system the first and last ``k``
    coefficients of a spline function are the same, respectively. It follows
    from the fact that all ``k - 1`` derivatives are equal term by term at ends
    and that the matrix of the original system of linear equations is
    non-degenerate. So, we can reduce the number of equations to ``n - 1``
    (first ``k - 1`` equations could be reduced). Another trick of this
    implementation is cyclic shift of values of B-splines due to equality of
    ``k`` unknown coefficients. With this we can receive matrix of the system
    with upper right and lower left blocks, and ``k`` diagonals.  It allows
    to use Woodbury formula to optimize the computations.

    '''
    n = y.shape[0]

    extradim = prod(y.shape[1:])
    y_new = y.reshape(n, extradim)
    c = np.zeros((n + k - 1, extradim))

    # n <= k case is solved with full matrix
    if n <= k:
        for i in range(extradim):
            c[:, i] = _make_interp_per_full_matr(x, y_new[:, i], t, k)
        c = np.ascontiguousarray(c.reshape((n + k - 1,) + y.shape[1:]))
        t, c = xp.asarray(t), xp.asarray(c)
        return BSpline.construct_fast(t, c, k, extrapolate='periodic', axis=axis)

    nt = len(t) - k - 1

    # size of block elements
    kul = int(k / 2)

    # kl = ku = k
    ab = np.zeros((3 * k + 1, nt), dtype=np.float64, order='F')

    # upper right and lower left blocks
    ur = np.zeros((kul, kul))
    ll = np.zeros_like(ur)

    # `offset` is made to shift all the non-zero elements to the end of the
    # matrix
    # NB: 1. drop the last element of `x` because `x[0] = x[-1] + T` & `y[0] == y[-1]`
    #     2. pass ab.T to _coloc to make it C-ordered; below it'll be fed to banded
    #        LAPACK, which needs F-ordered arrays
    _dierckx._coloc(x[:-1], t, k, ab.T, k)

    # remove zeros before the matrix
    ab = ab[-k - (k + 1) % 2:, :]

    # The least elements in rows (except repetitions) are diagonals
    # of block matrices. Upper right matrix is an upper triangular
    # matrix while lower left is a lower triangular one.
    for i in range(kul):
        ur += np.diag(ab[-i - 1, i: kul], k=i)
        ll += np.diag(ab[i, -kul - (k % 2): n - 1 + 2 * kul - i], k=-i)

    # remove elements that occur in the last point
    # (first and last points are equivalent)
    A = ab[:, kul: -k + kul]

    for i in range(extradim):
        cc = _woodbury_algorithm(A, ur, ll, y_new[:, i][:-1], k)
        c[:, i] = np.concatenate((cc[-kul:], cc, cc[:kul + k % 2]))
    c = np.ascontiguousarray(c.reshape((n + k - 1,) + y.shape[1:]))
    t, c = xp.asarray(t), xp.asarray(c)
    return BSpline.construct_fast(t, c, k, extrapolate='periodic', axis=axis)

