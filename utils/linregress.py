
def linregress(x, y=None):
    r"""
    Calculate a linear least-squares regression for two sets of measurements.

    Parameters
    ----------
    x, y : array_like
        Two sets of measurements.  Both arrays should have the same length N.  If
        only `x` is given (and ``y=None``), then it must be a two-dimensional
        array where one dimension has length 2.  The two sets of measurements
        are then found by splitting the array along the length-2 dimension. In
        the case where ``y=None`` and `x` is a 2xN array, ``linregress(x)`` is
        equivalent to ``linregress(x[0], x[1])``.

    Returns
    -------
    result : ``LinregressResult`` instance
        The return value is an object with the following attributes:

        slope : float
            Slope of the regression line.
        intercept : float
            Intercept of the regression line.
        rvalue : float
            The Pearson correlation coefficient. The square of ``rvalue``
            is equal to the coefficient of determination.
        pvalue : float
            The p-value for a hypothesis test whose null hypothesis is
            that the slope is zero, using Wald Test with t-distribution of
            the test statistic. See `alternative` above for alternative
            hypotheses.
        stderr : float
            Standard error of the estimated slope (gradient), under the
            assumption of residual normality.
        intercept_stderr : float
            Standard error of the estimated intercept, under the assumption
            of residual normality.

    See Also
    --------
    scipy.optimize.curve_fit :
        Use non-linear least squares to fit a function to data.
    scipy.optimize.leastsq :
        Minimize the sum of squares of a set of equations.

    Notes
    -----
    Missing values are considered pair-wise: if a value is missing in `x`,
    the corresponding value in `y` is masked.

    For compatibility with older versions of SciPy, the return value acts
    like a ``namedtuple`` of length 5, with fields ``slope``, ``intercept``,
    ``rvalue``, ``pvalue`` and ``stderr``, so one can continue to write::

        slope, intercept, r, p, se = linregress(x, y)

    With that style, however, the standard error of the intercept is not
    available.  To have access to all the computed values, including the
    standard error of the intercept, use the return value as an object
    with attributes, e.g.::

        result = linregress(x, y)
        print(result.intercept, result.intercept_stderr)

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats
    >>> rng = np.random.default_rng()

    Generate some data:

    >>> x = rng.random(10)
    >>> y = 1.6*x + rng.random(10)

    Perform the linear regression:

    >>> res = stats.mstats.linregress(x, y)

    Coefficient of determination (R-squared):

    >>> print(f"R-squared: {res.rvalue**2:.6f}")
    R-squared: 0.717533

    Plot the data along with the fitted line:

    >>> plt.plot(x, y, 'o', label='original data')
    >>> plt.plot(x, res.intercept + res.slope*x, 'r', label='fitted line')
    >>> plt.legend()
    >>> plt.show()

    Calculate 95% confidence interval on slope and intercept:

    >>> # Two-sided inverse Students t-distribution
    >>> # p - probability, df - degrees of freedom
    >>> from scipy.stats import t
    >>> tinv = lambda p, df: abs(t.ppf(p/2, df))

    >>> ts = tinv(0.05, len(x)-2)
    >>> print(f"slope (95%): {res.slope:.6f} +/- {ts*res.stderr:.6f}")
    slope (95%): 1.453392 +/- 0.743465
    >>> print(f"intercept (95%): {res.intercept:.6f}"
    ...       f" +/- {ts*res.intercept_stderr:.6f}")
    intercept (95%): 0.616950 +/- 0.544475

    """
    if y is None:
        x = ma.array(x)
        if x.shape[0] == 2:
            x, y = x
        elif x.shape[1] == 2:
            x, y = x.T
        else:
            raise ValueError("If only `x` is given as input, "
                             "it has to be of shape (2, N) or (N, 2), "
                             f"provided shape was {x.shape}")
    else:
        x = ma.array(x)
        y = ma.array(y)

    x = x.flatten()
    y = y.flatten()

    if np.amax(x) == np.amin(x) and len(x) > 1:
        raise ValueError("Cannot calculate a linear regression "
                         "if all x values are identical")

    m = ma.mask_or(ma.getmask(x), ma.getmask(y), shrink=False)
    if m is not nomask:
        x = ma.array(x, mask=m)
        y = ma.array(y, mask=m)
        if np.any(~m):
            result = _stats_py.linregress(x.data[~m], y.data[~m])
        else:
            # All data is masked
            result = _stats_py.LinregressResult(slope=None, intercept=None,
                                                rvalue=None, pvalue=None,
                                                stderr=None,
                                                intercept_stderr=None)
    else:
        result = _stats_py.linregress(x.data, y.data)

    return result


def linregress(x, y, alternative='two-sided', *, axis=0):
    """
    Calculate a linear least-squares regression for two sets of measurements.

    Parameters
    ----------
    x, y : array_like
        Two sets of measurements.  Both arrays should have the same length N.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the slope of the regression line is nonzero
        * 'less': the slope of the regression line is less than zero
        * 'greater':  the slope of the regression line is greater than zero

        .. versionadded:: 1.7.0
    axis : int or None, default: 0
        If an int, the axis of the input along which to compute the statistic.
        The statistic of each axis-slice (e.g. row) of the input will appear in a
        corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.

    Returns
    -------
    result : ``LinregressResult`` instance
        The return value is an object with the following attributes:

        slope : float
            Slope of the regression line.
        intercept : float
            Intercept of the regression line.
        rvalue : float
            The Pearson correlation coefficient. The square of ``rvalue``
            is equal to the coefficient of determination.
        pvalue : float
            The p-value for a hypothesis test whose null hypothesis is
            that the slope is zero, using Wald Test with t-distribution of
            the test statistic. See `alternative` above for alternative
            hypotheses.
        stderr : float
            Standard error of the estimated slope (gradient), under the
            assumption of residual normality.
        intercept_stderr : float
            Standard error of the estimated intercept, under the assumption
            of residual normality.

    See Also
    --------
    scipy.optimize.curve_fit :
        Use non-linear least squares to fit a function to data.
    scipy.optimize.leastsq :
        Minimize the sum of squares of a set of equations.

    Notes
    -----
    For compatibility with older versions of SciPy, the return value acts
    like a ``namedtuple`` of length 5, with fields ``slope``, ``intercept``,
    ``rvalue``, ``pvalue`` and ``stderr``, so one can continue to write::

        slope, intercept, r, p, se = linregress(x, y)

    With that style, however, the standard error of the intercept is not
    available.  To have access to all the computed values, including the
    standard error of the intercept, use the return value as an object
    with attributes, e.g.::

        result = linregress(x, y)
        print(result.intercept, result.intercept_stderr)

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats
    >>> rng = np.random.default_rng()

    Generate some data:

    >>> x = rng.random(10)
    >>> y = 1.6*x + rng.random(10)

    Perform the linear regression:

    >>> res = stats.linregress(x, y)

    Coefficient of determination (R-squared):

    >>> print(f"R-squared: {res.rvalue**2:.6f}")
    R-squared: 0.717533

    Plot the data along with the fitted line:

    >>> plt.plot(x, y, 'o', label='original data')
    >>> plt.plot(x, res.intercept + res.slope*x, 'r', label='fitted line')
    >>> plt.legend()
    >>> plt.show()

    Calculate 95% confidence interval on slope and intercept:

    >>> # Two-sided inverse Students t-distribution
    >>> # p - probability, df - degrees of freedom
    >>> from scipy.stats import t
    >>> tinv = lambda p, df: abs(t.ppf(p/2, df))

    >>> ts = tinv(0.05, len(x)-2)
    >>> print(f"slope (95%): {res.slope:.6f} +/- {ts*res.stderr:.6f}")
    slope (95%): 1.453392 +/- 0.743465
    >>> print(f"intercept (95%): {res.intercept:.6f}"
    ...       f" +/- {ts*res.intercept_stderr:.6f}")
    intercept (95%): 0.616950 +/- 0.544475

    """
    xp = array_namespace(x, y)
    x, y = xp_promote(x, y, force_floating=True, xp=xp)

    TINY = 1.0e-20

    # _axis_nan_policy decorator ensures that `axis=-1`
    x, y = _share_masks(x, y, xp=xp)
    n = _count_nonmasked(x, axis=-1, keepdims=False, xp=xp)
    xmean = xp.mean(x, axis=-1, keepdims=True)
    ymean = xp.mean(y, axis=-1, keepdims=True)

    # Average sums of square differences from the mean
    #   ssxm = mean( (x-mean(x))^2 )
    #   ssxym = mean( (x-mean(x)) * (y-mean(y)) )
    x_ = _demean(x, xmean, axis=-1, xp=xp)
    y_ = _demean(y, ymean, axis=-1, xp=xp, precision_warning=False)
    xmean = xp.squeeze(xmean, axis=-1)
    ymean = xp.squeeze(ymean, axis=-1)

    ssxm = xp.vecdot(x_, x_, axis=-1) / n
    ssym = xp.vecdot(y_, y_, axis=-1) / n
    ssxym = xp.vecdot(x_, y_, axis=-1) / n

    # R-value
    #   r = ssxym / sqrt( ssxm * ssym )
    degenerate = (ssxm == 0.0) | (ssym == 0.0)
    NaN = xp.asarray(xp.nan, dtype=ssxym.dtype)
    r = xpx.apply_where(
        ~degenerate,
        (ssxym, ssxm, ssym),
        lambda ssxym, ssxm, ssym: xp.clip(ssxym / xp.sqrt(ssxm * ssym), -1.0, 1.0),
        lambda ssxym, ssxm, ssym: xp.where(ssxym==0, NaN, 0.0)
    )

    slope = ssxym / ssxm
    intercept = ymean - slope*xmean
    with np.errstate(invalid='ignore', divide='ignore'):
        df = n - 2  # Number of degrees of freedom
        # n-2 degrees of freedom because 2 has been used up
        # to estimate the mean and standard deviation
        t = r * xp.sqrt(df / ((1.0 - r + TINY)*(1.0 + r + TINY)))

        dist = _SimpleStudentT(xp.asarray(df, dtype=t.dtype))
        prob = _get_pvalue(t, dist, alternative, xp=xp)
        prob = prob[()] if prob.ndim == 0 else prob

        slope_stderr = xp.sqrt((1 - r**2) * ssym / ssxm / df)

        # Also calculate the standard error of the intercept
        # The following relationship is used:
        #   ssxm = mean( (x-mean(x))^2 )
        #        = ssx - sx*sx
        #        = mean( x^2 ) - mean(x)^2
        intercept_stderr = slope_stderr * xp.sqrt(ssxm + xmean**2)

    outputs = slope, intercept, r, prob, slope_stderr, intercept_stderr
    outputs = (output[()] if output.ndim == 0 else output for output in outputs)
    slope, intercept, r, prob, slope_stderr, intercept_stderr = outputs

    return LinregressResult(slope=slope, intercept=intercept, rvalue=r,
                            pvalue=prob, stderr=slope_stderr,
                            intercept_stderr=intercept_stderr)

