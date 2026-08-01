
def chatterjeexi(x, y, *, axis=0, y_continuous=False, method='asymptotic'):
    r"""Compute the xi correlation and perform a test of independence.

    The xi correlation coefficient is a measure of association between two
    variables; the value tends to be close to zero when the variables are
    independent and close to 1 when there is a strong association. Unlike
    other correlation coefficients, the xi correlation is effective even
    when the association is not monotonic.

    Parameters
    ----------
    x, y : array-like
        The samples: corresponding observations of the independent and
        dependent variable. The (N-d) arrays must be broadcastable.
    axis : int, default: 0
        Axis along which to perform the test.
    y_continuous : bool, default: False
        Whether `y` is assumed to be drawn from a continuous distribution.
        If `y` is drawn from a continuous distribution, results are valid
        whether this is assumed or not, but enabling this assumption will
        result in faster computation and typically produce similar results.
    method : 'asymptotic' or `PermutationMethod` instance, optional
        Selects the method used to calculate the *p*-value.
        Default is 'asymptotic'. The following options are available.

        * ``'asymptotic'``: compares the standardized test statistic
          against the normal distribution.
        * `PermutationMethod` instance. In this case, the p-value
          is computed using `permutation_test` with the provided
          configuration options and other appropriate settings.

    Returns
    -------
    res : SignificanceResult
        An object containing attributes:

        statistic : float
            The xi correlation statistic.
        pvalue : float
            The associated *p*-value: the probability of a statistic at least as
            high as the observed value under the null hypothesis of independence.

    See Also
    --------
    scipy.stats.pearsonr, scipy.stats.spearmanr, scipy.stats.kendalltau

    Notes
    -----
    There is currently no special handling of ties in `x`; they are broken arbitrarily
    by the implementation. [1]_ recommends: "if there are ties among the Xi's, then
    choose an increasing rearrangement as above by breaking ties uniformly at random."
    This is easily accomplished by adding a small amount of random noise to `x`; see
    examples.

    [1]_ notes that the statistic is not symmetric in `x` and `y` *by design*:
    "...we may want to understand if :math:`Y` is a function :math:`X`, and not just
    if one of the variables is a function of the other." See [1]_ Remark 1.

    References
    ----------
    .. [1] Chatterjee, Sourav. "A new coefficient of correlation." Journal of
           the American Statistical Association 116.536 (2021): 2009-2022.
           :doi:`10.1080/01621459.2020.1758115`.

    Examples
    --------
    Generate perfectly correlated data, and observe that the xi correlation is
    nearly 1.0.

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng(348932549825235)
    >>> x = rng.uniform(0, 10, size=100)
    >>> y = np.sin(x)
    >>> res = stats.chatterjeexi(x, y)
    >>> res.statistic
    np.float64(0.9012901290129013)

    The probability of observing such a high value of the statistic under the
    null hypothesis of independence is very low.

    >>> res.pvalue
    np.float64(2.2206974648177804e-46)

    As noise is introduced, the correlation coefficient decreases.

    >>> noise = rng.normal(scale=[[0.1], [0.5], [1]], size=(3, 100))
    >>> res = stats.chatterjeexi(x, y + noise, axis=-1)
    >>> res.statistic
    array([0.79507951, 0.41824182, 0.16651665])

    Because the distribution of `y` is continuous, it is valid to pass
    ``y_continuous=True``. The statistic is identical, and the p-value
    (not shown) is only slightly different.

    >>> stats.chatterjeexi(x, y + noise, y_continuous=True, axis=-1).statistic
    array([0.79507951, 0.41824182, 0.16651665])

    Consider a case in which there are ties in `x`.

    >>> x = rng.integers(10, size=1000)
    >>> y = rng.integers(10, size=1000)

    [1]_ recommends breaking the ties uniformly at random.

    >>> d = rng.uniform(1e-5, size=x.size)
    >>> res = stats.chatterjeexi(x + d, y)
    >>> res.statistic
    -0.029919991638798438

    Since this gives a randomized estimate of the statistic, [1]_ also suggests
    considering the average over all possibilities of breaking ties. This is
    computationally infeasible when there are many ties, but a randomized estimate of
    *this* quantity can be obtained by considering many random possibilities of breaking
    ties.

    >>> d = rng.uniform(1e-5, size=(9999, x.size))
    >>> res = stats.chatterjeexi(x + d, y, axis=1)
    >>> np.mean(res.statistic)
    0.001186895213756626

    """
    xp = array_namespace(x, y)

    # x, y, `axis` input validation taken care of by decorator
    # In fact, `axis` is guaranteed to be -1
    y_continuous, method = _chatterjeexi_iv(y_continuous, method)
    x, y = xp_promote(x, y, force_floating=True, xp=xp)

    # A highly negative statistic is possible, e.g.
    # x = np.arange(100.), y = (x % 2 == 0)
    # Unclear whether we should expose `alternative`, though.
    alternative = 'greater'

    if method == 'asymptotic':
        xi, r, l = _xi_statistic(x, y, y_continuous, xp=xp)
        std = _xi_std(r, l, y_continuous, xp=xp)
        norm = _SimpleNormal()
        pvalue = _get_pvalue(xi / std, norm, alternative=alternative, xp=xp)
    elif isinstance(method, stats.PermutationMethod):
        res = stats.permutation_test(
            # Could be faster if we just permuted the ranks; for now, keep it simple.
            data=(y,),
            statistic=lambda y, axis: _xi_statistic(x, y, y_continuous, xp=xp)[0],
            alternative=alternative, permutation_type='pairings', **method._asdict(),
            axis=-1)  # `axis=-1` is guaranteed by _axis_nan_policy decorator

        xi, pvalue = res.statistic, res.pvalue

    xi = xi[()] if xi.ndim == 0 else xi
    pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue
    return SignificanceResult(xi, pvalue)

