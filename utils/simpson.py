
def simpson(y, x=None, *, dx=1.0, axis=-1):
    """
    Integrate y(x) using samples along the given axis and the composite
    Simpson's rule. If x is None, spacing of dx is assumed.

    Parameters
    ----------
    y : array_like
        Array to be integrated.
    x : array_like, optional
        If given, the points at which `y` is sampled.
    dx : float, optional
        Spacing of integration points along axis of `x`. Only used when
        `x` is None. Default is 1.
    axis : int, optional
        Axis along which to integrate. Default is the last axis.

    Returns
    -------
    float
        The estimated integral computed with the composite Simpson's rule.

    See Also
    --------
    quad : adaptive quadrature using QUADPACK
    fixed_quad : fixed-order Gaussian quadrature
    dblquad : double integrals
    tplquad : triple integrals
    romb : integrators for sampled data
    cumulative_trapezoid : cumulative integration for sampled data
    cumulative_simpson : cumulative integration using Simpson's 1/3 rule

    Notes
    -----
    For an odd number of samples that are equally spaced the result is
    exact if the function is a polynomial of order 3 or less. If
    the samples are not equally spaced, then the result is exact only
    if the function is a polynomial of order 2 or less.

    References
    ----------
    .. [1] Cartwright, Kenneth V. Simpson's Rule Cumulative Integration with
           MS Excel and Irregularly-spaced Data. Journal of Mathematical
           Sciences and Mathematics Education. 12 (2): 1-9

    Examples
    --------
    >>> from scipy import integrate
    >>> import numpy as np
    >>> x = np.arange(0, 10)
    >>> y = np.arange(0, 10)

    >>> integrate.simpson(y, x=x)
    40.5

    >>> y = np.power(x, 3)
    >>> integrate.simpson(y, x=x)
    1640.5
    >>> integrate.quad(lambda x: x**3, 0, 9)[0]
    1640.25

    """
    xp = array_namespace(y, x, dx)
    y, x, dx = xp_promote(y, x, dx, xp=xp)
    nd = y.ndim
    N = y.shape[axis]
    last_dx = dx
    if x is not None:
        if x.ndim == 1:
            shapex = [1] * nd
            shapex[axis] = x.shape[0]
            x = xp.reshape(x, tuple(shapex))
        elif x.ndim != y.ndim:
            raise ValueError("If given, shape of x must be 1-D or the same as y.")
        if x.shape[axis] != N:
            raise ValueError("If given, length of x along axis must be the same as y.")

    if N % 2 == 0:
        val = 0.0
        result = 0.0
        slice_all = (slice(None),) * nd

        if N == 2:
            # need at least 3 points in integration axis to form parabolic
            # segment. If there are two points then any of 'avg', 'first',
            # 'last' should give the same result.
            slice1 = tupleset(slice_all, axis, -1)
            slice2 = tupleset(slice_all, axis, -2)
            if x is not None:
                last_dx = x[slice1] - x[slice2]
            val = 0.5 * last_dx * (y[slice1] + y[slice2])
        else:
            # use Simpson's rule on first intervals
            result = _basic_simpson(y, 0, N-3, x, dx, axis, xp=xp)

            slice1 = tupleset(slice_all, axis, -1)
            slice2 = tupleset(slice_all, axis, -2)
            slice3 = tupleset(slice_all, axis, -3)

            h = xp.stack([dx, dx])
            if x is not None:
                # grab the last two spacings from the appropriate axis
                hm2 = tupleset(slice_all, axis, slice(-2, -1, 1))
                hm1 = tupleset(slice_all, axis, slice(-1, None, 1))

                diffs = xp.diff(x, axis=axis)
                h = [xp.squeeze(diffs[hm2], axis=axis),
                     xp.squeeze(diffs[hm1], axis=axis)]

            # This is the correction for the last interval according to
            # Cartwright.
            # However, I used the equations given at
            # https://en.wikipedia.org/wiki/Simpson%27s_rule#Composite_Simpson's_rule_for_irregularly_spaced_data
            # A footnote on Wikipedia says:
            # Cartwright 2017, Equation 8. The equation in Cartwright is
            # calculating the first interval whereas the equations in the
            # Wikipedia article are adjusting for the last integral. If the
            # proper algebraic substitutions are made, the equation results in
            # the values shown.
            num = 2 * h[1] ** 2 + 3 * h[0] * h[1]
            den = 6 * (h[1] + h[0])
            alpha = xpx.apply_where(den != 0, (num, den), xp.divide, fill_value=0.)

            num = h[1] ** 2 + 3.0 * h[0] * h[1]
            den = 6 * h[0]
            beta = xpx.apply_where(den != 0, (num, den), xp.divide, fill_value=0.)

            num = 1 * h[1] ** 3
            den = 6 * h[0] * (h[0] + h[1])
            eta = xpx.apply_where(den != 0, (num, den), xp.divide, fill_value=0.)

            result += alpha*y[slice1] + beta*y[slice2] - eta*y[slice3]

        result += val
    else:
        result = _basic_simpson(y, 0, N-2, x, dx, axis, xp=xp)
    return result

