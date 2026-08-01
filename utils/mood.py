
def mood(x, y, axis=0, alternative="two-sided"):
    """Perform Mood's test for equal scale parameters.

    Mood's two-sample test for scale parameters is a non-parametric
    test for the null hypothesis that two samples are drawn from the
    same distribution with the same scale parameter.

    Parameters
    ----------
    x, y : array_like
        Arrays of sample data. There must be at least three observations
        total.
    axis : int, optional
        The axis along which the samples are tested.  `x` and `y` can be of
        different length along `axis`.
        If `axis` is None, `x` and `y` are flattened and the test is done on
        all values in the flattened arrays.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the scales of the distributions underlying `x` and `y`
          are different.
        * 'less': the scale of the distribution underlying `x` is less than
          the scale of the distribution underlying `y`.
        * 'greater': the scale of the distribution underlying `x` is greater
          than the scale of the distribution underlying `y`.

        .. versionadded:: 1.7.0

    Returns
    -------
    res : SignificanceResult
        An object containing attributes:

        statistic : scalar or ndarray
            The z-score for the hypothesis test.  For 1-D inputs a scalar is
            returned.
        pvalue : scalar ndarray
            The p-value for the hypothesis test.

    See Also
    --------
    fligner : A non-parametric test for the equality of k variances
    ansari : A non-parametric test for the equality of 2 variances
    bartlett : A parametric test for equality of k variances in normal samples
    levene : A parametric test for equality of k variances

    Notes
    -----
    The data are assumed to be drawn from probability distributions ``f(x)``
    and ``f(x/s) / s`` respectively, for some probability density function f.
    The null hypothesis is that ``s == 1``.

    For multi-dimensional arrays, if the inputs are of shapes
    ``(n0, n1, n2, n3)``  and ``(n0, m1, n2, n3)``, then if ``axis=1``, the
    resulting z and p values will have shape ``(n0, n2, n3)``.  Note that
    ``n1`` and ``m1`` don't have to be equal, but the other dimensions do.

    References
    ----------
    [1] Mielke, Paul W. "Note on Some Squared Rank Tests with Existing Ties."
        Technometrics, vol. 9, no. 2, 1967, pp. 312-14. JSTOR,
        :doi:`10.2307/1266427`. Accessed 18 May 2022.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()
    >>> x2 = rng.standard_normal((2, 45, 6, 7))
    >>> x1 = rng.standard_normal((2, 30, 6, 7))
    >>> res = stats.mood(x1, x2, axis=1)
    >>> res.pvalue.shape
    (2, 6, 7)

    Find the number of points where the difference in scale is not significant:

    >>> (res.pvalue > 0.1).sum()
    78

    Perform the test with different scales:

    >>> x1 = rng.standard_normal((2, 30))
    >>> x2 = rng.standard_normal((2, 35)) * 10.0
    >>> stats.mood(x1, x2, axis=1)
    SignificanceResult(statistic=array([-5.76174136, -6.12650783]),
                       pvalue=array([8.32505043e-09, 8.98287869e-10]))

    """
    xp = array_namespace(x, y)
    x, y = xp_promote(x, y, force_floating=True, xp=xp)

    # _axis_nan_policy decorator ensures axis=-1
    xy = xp.concat((x, y), axis=-1)

    m = x.shape[-1]
    n = y.shape[-1]
    N = m + n

    if m == 0 or n == 0 or N < 3:  # only needed for test_axis_nan_policy
        NaN = _get_nan(x, y, xp=xp)
        return SignificanceResult(NaN, NaN)

    # determine if any of the samples contain ties
    # `a` represents ties within `x`; `t` represents ties within `xy`
    r, _, t = _stats_py._rankdata(xy, method='average', return_ties=True)

    if is_lazy_array(t) or xp.any(t > 1):
        z = _mood_statistic_with_ties(x, y, t, m, n, N, xp=xp)
    else:
        z = _mood_statistic_no_ties(r, m, n, N, xp=xp)

    pval = _get_pvalue(z, _SimpleNormal(), alternative, xp=xp)

    z = z[()] if z.ndim == 0 else z
    pval = pval[()] if pval.ndim == 0 else pval
    return SignificanceResult(z, pval)

