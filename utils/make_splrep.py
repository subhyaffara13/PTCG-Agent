
def make_splrep(x, y, *, w=None, xb=None, xe=None,
                k=3, s=0, t=None, nest=None, bc_type=None):
    r"""Create a smoothing B-spline function with bounded error, minimizing derivative jumps.

    Given the set of data points ``(x[i], y[i])``, determine a smooth spline
    approximation of degree ``k`` on the interval ``xb <= x <= xe``.

    Parameters
    ----------
    x, y : array_like, shape (m,)
        The data points defining a curve ``y = f(x)``.
    w : array_like, shape (m,), optional
        Strictly positive 1D array of weights, of the same length as `x` and `y`.
        The weights are used in computing the weighted least-squares spline
        fit. If the errors in the y values have standard-deviation given by the
        vector ``d``, then `w` should be ``1/d``.
        Default is ``np.ones(m)``.
    xb, xe : float, optional
        The interval to fit.  If None, these default to ``x[0]`` and ``x[-1]``,
        respectively.
    k : int, optional
        The degree of the spline fit. It is recommended to use cubic splines,
        ``k=3``, which is the default. Even values of `k` should be avoided,
        especially with small `s` values.
    s : float, optional
        The smoothing condition. The amount of smoothness is determined by
        satisfying the LSQ (least-squares) constraint::

            sum((w * (g(x)  - y))**2 ) <= s

        where ``g(x)`` is the smoothed fit to ``(x, y)``. The user can use `s`
        to control the tradeoff between closeness to data and smoothness of fit.
        Larger `s` means more smoothing while smaller values of `s` indicate less
        smoothing.
        Recommended values of `s` depend on the weights, `w`. If the weights
        represent the inverse of the standard deviation of `y`, then a good `s`
        value should be found in the range ``(m-sqrt(2*m), m+sqrt(2*m))`` where
        ``m`` is the number of datapoints in `x`, `y`, and `w`.
        Default is ``s = 0.0``, i.e. interpolation.
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
        For `s=0`,  ``spl(x) == y``.
        For non-zero values of `s` the `spl` represents the smoothed approximation
        to `(x, y)`, generally with fewer knots.

    See Also
    --------
    generate_knots : is used under the hood for generating the knots
    make_splprep : the analog of this routine for parametric curves
    make_interp_spline : construct an interpolating spline (``s = 0``)
    make_lsq_spline : construct the least-squares spline given the knot vector
    splrep : a FITPACK analog of this routine

    References
    ----------
    .. [1] P. Dierckx, "Algorithms for smoothing data with periodic and
        parametric splines, Computer Graphics and Image Processing",
        20 (1982) 171-184.
    .. [2] P. Dierckx, "Curve and surface fitting with splines", Monographs on
        Numerical Analysis, Oxford University Press, 1993.

    Notes
    -----
    This routine constructs the smoothing spline function, :math:`g(x)`, to
    minimize the sum of jumps, :math:`D_j`, of the ``k``-th derivative at the
    internal knots (:math:`x_b < t_i < x_e`), where

    .. math::

        D_i = g^{(k)}(t_i + 0) - g^{(k)}(t_i - 0)

    Specifically, the routine constructs the spline function :math:`g(x)` which
    minimizes

    .. math::

            \sum_i | D_i |^2 \to \mathrm{min}

    provided that

    .. math::

           \sum_{j=1}^m (w_j \times (g(x_j) - y_j))^2 \leqslant s ,

    where :math:`s > 0` is the input parameter.

    In other words, we balance maximizing the smoothness (measured as the jumps
    of the derivative, the first criterion), and the deviation of :math:`g(x_j)`
    from the data :math:`y_j` (the second criterion).

    Note that the summation in the second criterion is over all data points,
    and in the first criterion it is over the internal spline knots (i.e.
    those with ``xb < t[i] < xe``). The spline knots are in general a subset
    of data, see `generate_knots` for details.

    Also note the difference of this routine to `make_lsq_spline`: the latter
    routine does not consider smoothness and simply solves a least-squares
    problem

    .. math::

        \sum w_j \times (g(x_j) - y_j)^2 \to \mathrm{min}

    for a spline function :math:`g(x)` with a _fixed_ knot vector ``t``.

    .. versionadded:: 1.15.0
    """  # noqa:E501
    xp = array_namespace(x, y, w, t)
    if t is not None:
        t = xp.asarray(t)
    bc_type = _validate_bc_type(bc_type)

    if s == 0:
        if t is not None or w is not None or nest is not None:
            raise ValueError("s==0 is for interpolation only")
        return make_interp_spline(x, y, k=k, bc_type=bc_type)

    periodic = (bc_type == 'periodic')

    x, y, w, k, s, xb, xe = _validate_inputs(x, y, w, k, s, xb, xe,
                                             parametric=False, periodic=periodic)

    spl = _make_splrep_impl(x, y, w, xb, xe, k, s, t, nest, periodic, xp=xp)

    # postprocess: squeeze out the last dimension: was added to simplify the internals.
    spl.c = spl.c[:, 0]
    return spl

