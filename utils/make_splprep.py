
def make_splprep(x, *, w=None, u=None, ub=None, ue=None,
                 k=3, s=0, t=None, nest=None, bc_type=None):
    r"""
    Create a smoothing parametric B-spline curve with bounded error, minimizing derivative jumps.

    Given a list of N 1D arrays, `x`, which represent a curve in
    N-dimensional space parametrized by `u`, find a smooth approximating
    spline curve ``g(u)``.

    Parameters
    ----------
    x : array_like, shape (ndim, m)
        Sampled data points representing the curve in ``ndim`` dimensions.
        The typical use is a list of 1D arrays, each of length ``m``.
    w : array_like, shape(m,), optional
        Strictly positive 1D array of weights.
        The weights are used in computing the weighted least-squares spline
        fit. If the errors in the `x` values have standard deviation given by
        the vector d, then `w` should be 1/d. Default is ``np.ones(m)``.
    u : array_like, optional
        An array of parameter values for the curve in the parametric form.
        If not given, these values are calculated automatically, according to::

            v[0] = 0
            v[i] = v[i-1] + distance(x[i], x[i-1])
            u[i] = v[i] / v[-1]

    ub, ue : float, optional
        The end-points of the parameters interval. Default to ``u[0]`` and ``u[-1]``.
    k : int, optional
        Degree of the spline. Cubic splines, ``k=3``, are recommended.
        Even values of `k` should be avoided especially with a small ``s`` value.
        Default is ``k=3``
    s : float, optional
        A smoothing condition.  The amount of smoothness is determined by
        satisfying the conditions::

            sum((w * (g(u) - x))**2) <= s,

        where ``g(u)`` is the smoothed approximation to ``x``.  The user can
        use `s` to control the trade-off between closeness and smoothness
        of fit.  Larger ``s`` means more smoothing while smaller values of ``s``
        indicate less smoothing.
        Recommended values of ``s`` depend on the weights, ``w``.  If the weights
        represent the inverse of the standard deviation of ``x``, then a good
        ``s`` value should be found in the range ``(m - sqrt(2*m), m + sqrt(2*m))``,
        where ``m`` is the number of data points in ``x`` and ``w``.
    t : array_like, optional
        The spline knots. If None (default), the knots will be constructed
        automatically.
        There must be at least ``2*k + 2`` and at most ``m + k + 1`` knots.
    nest : int, optional
        The target length of the knot vector. Should be between ``2*(k + 1)``
        (the minimum number of knots for a degree-``k`` spline), and
        ``m + k + 1`` (the number of knots of the interpolating spline).
        The actual number of knots returned by this routine may be slightly
        larger than `nest`.
        Default is None (no limit, add up to ``m + k + 1`` knots).
    bc_type : str, optional
        Boundary conditions.
        Default is `"not-a-knot"`.
        The following boundary conditions are recognized:

        * ``"not-a-knot"`` (default): The first and second segments are the
          same polynomial. This is equivalent to having ``bc_type=None``.
        * ``"periodic"``: The values and the first ``k-1`` derivatives at the
          ends are equivalent.

    Returns
    -------
    spl : a `BSpline` instance
        For `s=0`,  ``spl(u) == x``.
        For non-zero values of ``s``, `spl` represents the smoothed approximation
        to ``x``, generally with fewer knots.
    u : ndarray
        The values of the parameters

    See Also
    --------
    generate_knots : is used under the hood for generating the knots
    make_splrep : the analog of this routine 1D functions
    make_interp_spline : construct an interpolating spline (``s = 0``)
    make_lsq_spline : construct the least-squares spline given the knot vector
    splprep : a FITPACK analog of this routine

    Notes
    -----
    Given a set of :math:`m` data points in :math:`D` dimensions, :math:`\vec{x}_j`,
    with :math:`j=1, ..., m` and :math:`\vec{x}_j = (x_{j; 1}, ..., x_{j; D})`,
    this routine constructs the parametric spline curve :math:`g_a(u)` with
    :math:`a=1, ..., D`, to minimize the sum of jumps, :math:`D_{i; a}`, of the
    ``k``-th derivative at the internal knots (:math:`u_b < t_i < u_e`), where

    .. math::

        D_{i; a} = g_a^{(k)}(t_i + 0) - g_a^{(k)}(t_i - 0)

    Specifically, the routine constructs the spline function :math:`g(u)` which
    minimizes

    .. math::

            \sum_i \sum_{a=1}^D | D_{i; a} |^2 \to \mathrm{min}

    provided that

    .. math::

        \sum_{j=1}^m \sum_{a=1}^D (w_j \times (g_a(u_j) - x_{j; a}))^2 \leqslant s

    where :math:`u_j` is the value of the parameter corresponding to the data point
    :math:`(x_{j; 1}, ..., x_{j; D})`, and :math:`s > 0` is the input parameter.

    In other words, we balance maximizing the smoothness (measured as the jumps
    of the derivative, the first criterion), and the deviation of :math:`g(u_j)`
    from the data :math:`x_j` (the second criterion).

    Note that the summation in the second criterion is over all data points,
    and in the first criterion it is over the internal spline knots (i.e.
    those with ``ub < t[i] < ue``). The spline knots are in general a subset
    of data, see `generate_knots` for details.

    .. versionadded:: 1.15.0

    References
    ----------
    .. [1] P. Dierckx, "Algorithms for smoothing data with periodic and
        parametric splines, Computer Graphics and Image Processing",
        20 (1982) 171-184.
    .. [2] P. Dierckx, "Curve and surface fitting with splines", Monographs on
        Numerical Analysis, Oxford University Press, 1993.
    """  # noqa:E501

    bc_type = _validate_bc_type(bc_type)

    periodic = (bc_type == 'periodic')

    # x can be either a 2D array or a list of 1D arrays
    if isinstance(x, list):
        xp = array_namespace(*x, w, u, t)
    else:
        xp = array_namespace(x, w, u, t)

    x = xp.stack(x, axis=1)

    # construct the default parametrization of the curve
    if u is None:
        dp = (x[1:, :] - x[:-1, :])**2
        u = xp.cumulative_sum( xp.sqrt(xp.sum(dp, axis=1)) )
        u = concat_1d(xp, 0., u / u[-1])

    if s == 0:
        if t is not None or w is not None or nest is not None:
            raise ValueError("s==0 is for interpolation only")
        return make_interp_spline(u, x.T, k=k, axis=1), u

    u, x, w, k, s, ub, ue = _validate_inputs(u, x, w, k, s, ub, ue,
                                             parametric=True, periodic=periodic)

    if t is not None:
        t = xp.asarray(t)

    spl = _make_splrep_impl(u, x, w, ub, ue, k, s, t,
                            nest, periodic=periodic, xp=xp)

    # posprocess: `axis=1` so that spl(u).shape == np.shape(x)
    # when `x` is a list of 1D arrays (cf original splPrep)
    cc = spl.c.T
    spl1 = BSpline(spl.t, cc, spl.k, axis=1)

    return spl1, xp.asarray(u)

