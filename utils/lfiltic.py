
def lfiltic(b, a, y, x=None):
    """
    Construct initial conditions for lfilter given input and output vectors.

    Given a linear filter (b, a) and initial conditions on the output `y`
    and the input `x`, return the initial conditions on the state vector zi
    which is used by `lfilter` to generate the output given the input.

    Parameters
    ----------
    b : array_like
        Linear filter term.
    a : array_like
        Linear filter term.
    y : array_like
        Initial conditions.

        If ``N = len(a) - 1``, then ``y = {y[-1], y[-2], ..., y[-N]}``.

        If `y` is too short, it is padded with zeros.
    x : array_like, optional
        Initial conditions.

        If ``M = len(b) - 1``, then ``x = {x[-1], x[-2], ..., x[-M]}``.

        If `x` is not given, its initial conditions are assumed zero.

        If `x` is too short, it is padded with zeros.

    Returns
    -------
    zi : ndarray
        The state vector ``zi = {z_0[-1], z_1[-1], ..., z_K-1[-1]}``,
        where ``K = max(M, N)``.

    See Also
    --------
    lfilter, lfilter_zi

    """
    xp = array_namespace(a, b, y, x)

    a = xpx.atleast_nd(xp.asarray(a), ndim=1, xp=xp)
    b = xpx.atleast_nd(xp.asarray(b), ndim=1, xp=xp)
    if a.ndim > 1:
        raise ValueError('Filter coefficients `a` must be 1-D.')
    if b.ndim > 1:
        raise ValueError('Filter coefficients `b` must be 1-D.')
    N = a.shape[0] - 1
    M = b.shape[0] - 1
    K = max(M, N)
    y = xp.asarray(y)

    if N < 0:
        raise ValueError("There must be at least one `a` coefficient.")

    if x is None:
        result_type = xp.result_type(b, a, y)
        if xp.isdtype(result_type, ('bool', 'integral')):  #'bui':
            result_type = xp.float64
        x = xp.zeros(M, dtype=result_type)
    else:
        x = xp.asarray(x)

        result_type = xp.result_type(b, a, y, x)
        if xp.isdtype(result_type, ('bool', 'integral')):  #'bui':
            result_type = xp.float64
        x = xp.astype(x, result_type)

        L = xp_size(x)
        if L < M:
            x = xp.concat((x, xp.zeros(M - L)))

    y = xp.astype(y, result_type)
    zi = xp.zeros(K, dtype=result_type)

    L = xp_size(y)
    if L < N:
        y = xp.concat((y, xp.zeros(N - L)))

    for m in range(M):
        zi[m] = xp.sum(b[m + 1:] * x[:M - m], axis=0)

    for m in range(N):
        zi[m] -= xp.sum(a[m + 1:] * y[:N - m], axis=0)

    if a[0] != 1.:
        if a[0] == 0.:
            raise ValueError("First `a` filter coefficient must be non-zero.")
        zi /= a[0]

    return zi

