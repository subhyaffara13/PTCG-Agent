
def make_lsq_spline(x, y, t, k=3, w=None, axis=0, check_finite=True, *, method="qr"):
    r"""Create a smoothing B-spline satisfying the Least SQuares (LSQ) criterion.

    The result is a linear combination

    .. math::

            S(x) = \sum_j c_j B_j(x; t)

    of the B-spline basis elements, :math:`B_j(x; t)`, which minimizes

    .. math::

        \sum_{j} \left( w_j \times (S(x_j) - y_j) \right)^2

    Parameters
    ----------
    x : array_like, shape (m,)
        Abscissas.
    y : array_like, shape (m, ...)
        Ordinates.
    t : array_like, shape (n + k + 1,)
        Knots.
        Knots and data points must satisfy Schoenberg-Whitney conditions.
    k : int, optional
        B-spline degree. Default is cubic, ``k = 3``.
    w : array_like, shape (m,), optional
        Weights for spline fitting. Must be positive. If ``None``,
        then weights are all equal.
        Default is ``None``.
    axis : int, optional
        Interpolation axis. Default is zero.
    check_finite : bool, optional
        Whether to check that the input arrays contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
        Default is True.
    method : str, optional
        Method for solving the linear LSQ problem. Allowed values are "norm-eq"
        (Explicitly construct and solve the normal system of equations), and
        "qr" (Use the QR factorization of the design matrix).
        Default is "qr".

    Returns
    -------
    b : `BSpline` object
        A `BSpline` object of the degree ``k`` with knots ``t``.

    See Also
    --------
    BSpline : base class representing the B-spline objects
    make_interp_spline : a similar factory function for interpolating splines
    LSQUnivariateSpline : a FITPACK-based spline fitting routine
    splrep : a FITPACK-based fitting routine

    Notes
    -----
    The number of data points must be larger than the spline degree ``k``.

    Knots ``t`` must satisfy the Schoenberg-Whitney conditions,
    i.e., there must be a subset of data points ``x[j]`` such that
    ``t[j] < x[j] < t[j+k+1]``, for ``j=0, 1,...,n-k-2``.

    Examples
    --------
    Generate some noisy data:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()
    >>> x = np.linspace(-3, 3, 50)
    >>> y = np.exp(-x**2) + 0.1 * rng.standard_normal(50)

    Now fit a smoothing cubic spline with a pre-defined internal knots.
    Here we make the knot vector (k+1)-regular by adding boundary knots:

    >>> from scipy.interpolate import make_lsq_spline, BSpline
    >>> t = [-1, 0, 1]
    >>> k = 3
    >>> t = np.r_[(x[0],)*(k+1),
    ...           t,
    ...           (x[-1],)*(k+1)]
    >>> spl = make_lsq_spline(x, y, t, k)

    For comparison, we also construct an interpolating spline for the same
    set of data:

    >>> from scipy.interpolate import make_interp_spline
    >>> spl_i = make_interp_spline(x, y)

    Plot both:

    >>> xs = np.linspace(-3, 3, 100)
    >>> plt.plot(x, y, 'ro', ms=5)
    >>> plt.plot(xs, spl(xs), 'g-', lw=3, label='LSQ spline')
    >>> plt.plot(xs, spl_i(xs), 'b-', lw=3, alpha=0.7, label='interp spline')
    >>> plt.legend(loc='best')
    >>> plt.show()

    **NaN handling**: If the input arrays contain ``nan`` values, the result is
    not useful since the underlying spline fitting routines cannot deal with
    ``nan``. A workaround is to use zero weights for not-a-number data points:

    >>> y[8] = np.nan
    >>> w = np.isnan(y)
    >>> y[w] = 0.
    >>> tck = make_lsq_spline(x, y, t, w=~w)

    Notice the need to replace a ``nan`` by a numerical value (precise value
    does not matter as long as the corresponding weight is zero.)

    """
    xp = array_namespace(x, y, t, w)

    x = _as_float_array(x, check_finite)
    y = _as_float_array(y, check_finite)
    t = _as_float_array(t, check_finite)
    if w is not None:
        w = _as_float_array(w, check_finite)
    else:
        w = np.ones_like(x)
    k = operator.index(k)

    axis = normalize_axis_index(axis, y.ndim)

    y = np.moveaxis(y, axis, 0)    # now internally interp axis is zero
    if not y.flags.c_contiguous:
        # C routines in _dierckx currently require C contiguity
        y = y.copy(order='C')

    if x.ndim != 1:
        raise ValueError("Expect x to be a 1-D sequence.")
    if x.shape[0] < k+1:
        raise ValueError("Need more x points.")
    if k < 0:
        raise ValueError("Expect non-negative k.")
    if t.ndim != 1 or np.any(t[1:] - t[:-1] < 0):
        raise ValueError("Expect t to be a 1D strictly increasing sequence.")
    if x.size != y.shape[0]:
        raise ValueError(f'Shapes of x {x.shape} and y {y.shape} are incompatible')
    if k > 0 and np.any((x < t[k]) | (x > t[-k])):
        raise ValueError(f'Out of bounds w/ x = {x}.')
    if x.size != w.size:
        raise ValueError(f'Shapes of x {x.shape} and w {w.shape} are incompatible')
    if method == "norm-eq" and np.any(x[1:] - x[:-1] <= 0):
        raise ValueError("Expect x to be a 1D strictly increasing sequence.")
    if method == "qr" and any(x[1:] - x[:-1] < 0):
        raise ValueError("Expect x to be a 1D non-decreasing sequence.")

    # number of coefficients
    n = t.size - k - 1

    # complex y: view as float, preserve the length
    was_complex =  y.dtype.kind == 'c'
    yy = y.view(float)
    if was_complex and y.ndim == 1:
        yy = yy.reshape(y.shape[0], 2)

    # multiple r.h.s
    extradim = prod(yy.shape[1:])
    yy = yy.reshape(-1, extradim)

    # complex y: view as float, preserve the length
    was_complex =  y.dtype.kind == 'c'
    yy = y.view(float)
    if was_complex and y.ndim == 1:
        yy = yy.reshape(y.shape[0], 2)

    # multiple r.h.s
    extradim = prod(yy.shape[1:])
    yy = yy.reshape(-1, extradim)

    if method == "norm-eq":
        # construct A.T @ A and rhs with A the colocation matrix, and
        # rhs = A.T @ y for solving the LSQ problem  ``A.T @ A @ c = A.T @ y``
        lower = True
        ab = np.zeros((k+1, n), dtype=np.float64, order='F')
        rhs = np.zeros((n, extradim), dtype=np.float64)
        _dierckx._norm_eq_lsq(x, t, k,
                              yy,
                              w,
                              ab.T, rhs)

        # undo complex -> float and flattening the trailing dims
        if was_complex:
            rhs = rhs.view(complex)

        rhs = rhs.reshape((n,) + y.shape[1:])

        # have observation matrix & rhs, can solve the LSQ problem
        cho_decomp = cholesky_banded(ab, overwrite_ab=True, lower=lower,
                                     check_finite=check_finite)
        m = rhs.shape[0]
        c = cho_solve_banded((cho_decomp, lower), rhs.reshape(m, -1), overwrite_b=True,
                             check_finite=check_finite).reshape(rhs.shape)
    elif method == "qr":
        _, _, c, _, _ = _lsq_solve_qr(x, yy, t, k, w)

        if was_complex:
            c = c.view(complex)

    else:
        raise ValueError(f"Unknown {method =}.")


    # restore the shape of `c` for both single and multiple r.h.s.
    c = c.reshape((n,) + y.shape[1:])
    c = np.ascontiguousarray(c)
    t, c = xp.asarray(t), xp.asarray(c)
    return BSpline.construct_fast(t, c, k, axis=axis)

