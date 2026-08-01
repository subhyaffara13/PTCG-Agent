
def spearmanrho(x, y, /, *, alternative='two-sided', method=None, axis=0):
    r"""Calculate a Spearman rho correlation coefficient with associated p-value.

    The Spearman rank-order correlation coefficient is a nonparametric measure
    of the monotonicity of the relationship between two datasets.
    Like other correlation coefficients, it varies between -1 and +1 with 0
    implying no correlation. Coefficients of -1 or +1 are associated with an exact
    monotonic relationship.  Positive correlations indicate that as `x` increases,
    so does `y`; negative correlations indicate that as `x` increases, `y` decreases.
    The p-value is the probability of an uncorrelated system producing datasets
    with a Spearman correlation at least as extreme as the one computed from the
    observed dataset.

    Parameters
    ----------
    x, y : array-like
        The samples: corresponding observations of the independent and
        dependent variable. The (N-d) arrays must be broadcastable.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the correlation is nonzero
        * 'less': the correlation is negative (less than zero)
        * 'greater':  the correlation is positive (greater than zero)

    method : ResamplingMethod, optional
        Defines the method used to compute the p-value. If `method` is an
        instance of `PermutationMethod`/`MonteCarloMethod`, the p-value is
        computed using
        `scipy.stats.permutation_test`/`scipy.stats.monte_carlo_test` with the
        provided configuration options and other appropriate settings.
        Otherwise, the p-value is computed using an asymptotic approximation of
        the null distribution.
    axis : int or None, optional
        If axis=0 (default), then each column represents a variable, with
        observations in the rows. If axis=1, the relationship is transposed:
        each row represents a variable, while the columns contain observations.
        If axis=None, then both arrays will be raveled.
        Like other `scipy.stats` functions, `axis` is interpreted after the
        arrays are broadcasted.

    Returns
    -------
    res : SignificanceResult
        An object containing attributes:

        statistic : floating point array or NumPy scalar
            Spearman correlation coefficient
        pvalue : floating point array NumPy scalar
            The p-value - the probabilitiy of realizing such an extreme statistic
            value under the null hypothesis that two samples have no ordinal
            correlation. See `alternative` above for alternative hypotheses.

    Warns
    -----
    `~scipy.stats.ConstantInputWarning`
        Raised if an input is a constant array.  The correlation coefficient
        is not defined in this case, so ``np.nan`` is returned.

    Notes
    -----
    `spearmanrho` was created to make improvements to SciPy's implementation of
    the Spearman correlation test without making backward-incompatible changes
    to `spearmanr`. Advantages of `spearmanrho` over `spearmanr` include:

    - `spearmanrho` follows standard array broadcasting rules.
    - `spearmanrho` is compatible with some non-NumPy arrays.
    - `spearmanrho` can compute exact p-values, even in the presence of ties,
      when an appropriate instance of `PermutationMethod` is provided via the
      `method` argument.

    References
    ----------
    .. [1] Zwillinger, D. and Kokoska, S. (2000). CRC Standard
       Probability and Statistics Tables and Formulae. Chapman & Hall: New
       York. 2000.
       Section  14.7
    .. [2] Kendall, M. G. and Stuart, A. (1973).
       The Advanced Theory of Statistics, Volume 2: Inference and Relationship.
       Griffin. 1973.
       Section 31.18

    Examples
    --------
    Univariate samples, approximate p-value.

    >>> import numpy as np
    >>> from scipy import stats
    >>> x = [1, 2, 3, 4, 5]
    >>> y = [5, 6, 7, 8, 7]
    >>> res = stats.spearmanrho(x, y)
    >>> res.statistic
    np.float64(0.8207826816681233)
    >>> res.pvalue
    np.float64(0.08858700531354405)

    Univariate samples, exact p-value.

    >>> res = stats.spearmanrho(x, y, method=stats.PermutationMethod())
    >>> res.statistic
    np.float64(0.8207826816681233)
    >>> res.pvalue
    np.float64(0.13333333333333333)

    Batch of univariate samples, one vectorized call.

    >>> rng = np.random.default_rng(98145152315484)
    >>> x2 = rng.standard_normal((2, 100))
    >>> y2 = rng.standard_normal((2, 100))
    >>> res = stats.spearmanrho(x2, y2, axis=-1)
    >>> res.statistic
    array([ 0.16585659, -0.12151215])
    >>> res.pvalue
    array([0.0991155 , 0.22846869])

    Bivariate samples using standard broadcasting rules.

    >>> res = stats.spearmanrho(x2[np.newaxis, :], x2[:, np.newaxis], axis=-1)
    >>> res.statistic
    array([[ 1.        , -0.14670267],
           [-0.14670267,  1.        ]])
    >>> res.pvalue
    array([[0.        , 0.14526128],
           [0.14526128, 0.        ]])

    """
    xp = array_namespace(x, y)
    x, y = _share_masks(x, y, xp=xp)
    rx = stats.rankdata(x, axis=axis)
    ry = stats.rankdata(y, axis=axis)
    res = stats.pearsonr(rx, ry, method=method, alternative=alternative, axis=axis)
    return SignificanceResult(res.statistic, res.pvalue)

