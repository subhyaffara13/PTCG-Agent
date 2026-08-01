
def spearmanr(x, y=None, use_ties=True, axis=None, nan_policy='propagate',
              alternative='two-sided'):
    """
    Calculates a Spearman rank-order correlation coefficient and the p-value
    to test for non-correlation.

    The Spearman correlation is a nonparametric measure of the linear
    relationship between two datasets. Unlike the Pearson correlation, the
    Spearman correlation does not assume that both datasets are normally
    distributed. Like other correlation coefficients, this one varies
    between -1 and +1 with 0 implying no correlation. Correlations of -1 or
    +1 imply a monotonic relationship. Positive correlations imply that
    as `x` increases, so does `y`. Negative correlations imply that as `x`
    increases, `y` decreases.

    Missing values are discarded pair-wise: if a value is missing in `x`, the
    corresponding value in `y` is masked.

    The p-value roughly indicates the probability of an uncorrelated system
    producing datasets that have a Spearman correlation at least as extreme
    as the one computed from these datasets. The p-values are not entirely
    reliable but are probably reasonable for datasets larger than 500 or so.

    Parameters
    ----------
    x, y : 1D or 2D array_like, y is optional
        One or two 1-D or 2-D arrays containing multiple variables and
        observations. When these are 1-D, each represents a vector of
        observations of a single variable. For the behavior in the 2-D case,
        see under ``axis``, below.
    use_ties : bool, optional
        DO NOT USE.  Does not do anything, keyword is only left in place for
        backwards compatibility reasons.
    axis : int or None, optional
        If axis=0 (default), then each column represents a variable, with
        observations in the rows. If axis=1, the relationship is transposed:
        each row represents a variable, while the columns contain observations.
        If axis=None, then both arrays will be raveled.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the correlation is nonzero
        * 'less': the correlation is negative (less than zero)
        * 'greater':  the correlation is positive (greater than zero)

        .. versionadded:: 1.7.0

    Returns
    -------
    res : SignificanceResult
        An object containing attributes:

        statistic : float or ndarray (2-D square)
            Spearman correlation matrix or correlation coefficient (if only 2
            variables are given as parameters). Correlation matrix is square
            with length equal to total number of variables (columns or rows) in
            ``a`` and ``b`` combined.
        pvalue : float
            The p-value for a hypothesis test whose null hypothesis
            is that two sets of data are linearly uncorrelated. See
            `alternative` above for alternative hypotheses. `pvalue` has the
            same shape as `statistic`.

    References
    ----------
    [CRCProbStat2000] section 14.7

    """
    if not use_ties:
        raise ValueError("`use_ties=False` is not supported in SciPy >= 1.2.0")

    # Always returns a masked array, raveled if axis=None
    x, axisout = _chk_asarray(x, axis)
    if y is not None:
        # Deal only with 2-D `x` case.
        y, _ = _chk_asarray(y, axis)
        if axisout == 0:
            x = ma.column_stack((x, y))
        else:
            x = ma.vstack((x, y))

    if axisout == 1:
        # To simplify the code that follow (always use `n_obs, n_vars` shape)
        x = x.T

    if nan_policy == 'omit':
        x = ma.masked_invalid(x)

    def _spearmanr_2cols(x):
        # Mask the same observations for all variables, and then drop those
        # observations (can't leave them masked, rankdata is weird).
        x = ma.mask_rowcols(x, axis=0)
        x = x[~x.mask.any(axis=1), :]

        # If either column is entirely NaN or Inf
        if not np.any(x.data):
            res = scipy.stats._stats_py.SignificanceResult(np.nan, np.nan)
            res.correlation = np.nan
            return res

        m = ma.getmask(x)
        n_obs = x.shape[0]
        dof = n_obs - 2 - int(m.sum(axis=0)[0])
        if dof < 0:
            raise ValueError("The input must have at least 3 entries!")

        # Gets the ranks and rank differences
        x_ranked = rankdata(x, axis=0)
        rs = ma.corrcoef(x_ranked, rowvar=False).data

        # rs can have elements equal to 1, so avoid zero division warnings
        with np.errstate(divide='ignore'):
            # clip the small negative values possibly caused by rounding
            # errors before taking the square root
            t = rs * np.sqrt((dof / ((rs+1.0) * (1.0-rs))).clip(0))

        t, prob = _ttest_finish(dof, t, alternative)

        # For backwards compatibility, return scalars when comparing 2 columns
        if rs.shape == (2, 2):
            res = scipy.stats._stats_py.SignificanceResult(rs[1, 0],
                                                           prob[1, 0])
            res.correlation = rs[1, 0]
            return res
        else:
            res = scipy.stats._stats_py.SignificanceResult(rs, prob)
            res.correlation = rs
            return res

    # Need to do this per pair of variables, otherwise the dropped observations
    # in a third column mess up the result for a pair.
    n_vars = x.shape[1]
    if n_vars == 2:
        return _spearmanr_2cols(x)
    else:
        rs = np.ones((n_vars, n_vars), dtype=float)
        prob = np.zeros((n_vars, n_vars), dtype=float)
        for var1 in range(n_vars - 1):
            for var2 in range(var1+1, n_vars):
                result = _spearmanr_2cols(x[:, [var1, var2]])
                rs[var1, var2] = result.correlation
                rs[var2, var1] = result.correlation
                prob[var1, var2] = result.pvalue
                prob[var2, var1] = result.pvalue

        res = scipy.stats._stats_py.SignificanceResult(rs, prob)
        res.correlation = rs
        return res


def spearmanr(a, b=None, axis=0, nan_policy='propagate',
              alternative='two-sided'):
    r"""Calculate a Spearman correlation coefficient with associated p-value.

    The Spearman rank-order correlation coefficient is a nonparametric measure
    of the monotonicity of the relationship between two datasets.
    Like other correlation coefficients,
    this one varies between -1 and +1 with 0 implying no correlation.
    Correlations of -1 or +1 imply an exact monotonic relationship. Positive
    correlations imply that as x increases, so does y. Negative correlations
    imply that as x increases, y decreases.

    The p-value roughly indicates the probability of an uncorrelated system
    producing datasets that have a Spearman correlation at least as extreme
    as the one computed from these datasets. Although calculation of the
    p-value does not make strong assumptions about the distributions underlying
    the samples, it is only accurate for very large samples (>500
    observations). For smaller sample sizes, consider a permutation test (see
    Examples section below).

    Parameters
    ----------
    a, b : 1D or 2D array_like, b is optional
        One or two 1-D or 2-D arrays containing multiple variables and
        observations. When these are 1-D, each represents a vector of
        observations of a single variable. For the behavior in the 2-D case,
        see under ``axis``, below.
        Both arrays need to have the same length in the ``axis`` dimension.
    axis : int or None, optional
        If axis=0 (default), then each column represents a variable, with
        observations in the rows. If axis=1, the relationship is transposed:
        each row represents a variable, while the columns contain observations.
        If axis=None, then both arrays will be raveled.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the correlation is nonzero
        * 'less': the correlation is negative (less than zero)
        * 'greater':  the correlation is positive (greater than zero)

        .. versionadded:: 1.7.0

    Returns
    -------
    res : SignificanceResult
        An object containing attributes:

        statistic : float or ndarray (2-D square)
            Spearman correlation matrix or correlation coefficient (if only 2
            variables are given as parameters). Correlation matrix is square
            with length equal to total number of variables (columns or rows) in
            ``a`` and ``b`` combined.
        pvalue : float
            The p-value for a hypothesis test whose null hypothesis
            is that two samples have no ordinal correlation. See
            `alternative` above for alternative hypotheses. `pvalue` has the
            same shape as `statistic`.

    Raises
    ------
    ValueError
        If `axis` is not 0, 1 or None, or if the number of dimensions of `a`
        is greater than 2, or if `b` is None and the number of dimensions of
        `a` is less than 2.

    Warns
    -----
    `~scipy.stats.ConstantInputWarning`
        Raised if an input is a constant array.  The correlation coefficient
        is not defined in this case, so ``np.nan`` is returned.

    See Also
    --------
    :ref:`hypothesis_spearmanr` : Extended example

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

    >>> import numpy as np
    >>> from scipy import stats
    >>> res = stats.spearmanr([1, 2, 3, 4, 5], [5, 6, 7, 8, 7])
    >>> res.statistic
    0.8207826816681233
    >>> res.pvalue
    0.08858700531354381

    >>> rng = np.random.default_rng()
    >>> x2n = rng.standard_normal((100, 2))
    >>> y2n = rng.standard_normal((100, 2))
    >>> res = stats.spearmanr(x2n)
    >>> res.statistic, res.pvalue
    (-0.07960396039603959, 0.4311168705769747)

    >>> res = stats.spearmanr(x2n[:, 0], x2n[:, 1])
    >>> res.statistic, res.pvalue
    (-0.07960396039603959, 0.4311168705769747)

    >>> res = stats.spearmanr(x2n, y2n)
    >>> res.statistic
    array([[ 1. , -0.07960396, -0.08314431, 0.09662166],
           [-0.07960396, 1. , -0.14448245, 0.16738074],
           [-0.08314431, -0.14448245, 1. , 0.03234323],
           [ 0.09662166, 0.16738074, 0.03234323, 1. ]])
    >>> res.pvalue
    array([[0. , 0.43111687, 0.41084066, 0.33891628],
           [0.43111687, 0. , 0.15151618, 0.09600687],
           [0.41084066, 0.15151618, 0. , 0.74938561],
           [0.33891628, 0.09600687, 0.74938561, 0. ]])

    >>> res = stats.spearmanr(x2n.T, y2n.T, axis=1)
    >>> res.statistic
    array([[ 1. , -0.07960396, -0.08314431, 0.09662166],
           [-0.07960396, 1. , -0.14448245, 0.16738074],
           [-0.08314431, -0.14448245, 1. , 0.03234323],
           [ 0.09662166, 0.16738074, 0.03234323, 1. ]])

    >>> res = stats.spearmanr(x2n, y2n, axis=None)
    >>> res.statistic, res.pvalue
    (0.044981624540613524, 0.5270803651336189)

    >>> res = stats.spearmanr(x2n.ravel(), y2n.ravel())
    >>> res.statistic, res.pvalue
    (0.044981624540613524, 0.5270803651336189)

    >>> rng = np.random.default_rng()
    >>> xint = rng.integers(10, size=(100, 2))
    >>> res = stats.spearmanr(xint)
    >>> res.statistic, res.pvalue
    (0.09800224850707953, 0.3320271757932076)

    For small samples, consider performing a permutation test instead of
    relying on the asymptotic p-value. Note that to calculate the null
    distribution of the statistic (for all possibly pairings between
    observations in sample ``x`` and ``y``), only one of the two inputs needs
    to be permuted.

    >>> x = [1.76405235, 0.40015721, 0.97873798,
    ... 2.2408932, 1.86755799, -0.97727788]
    >>> y = [2.71414076, 0.2488, 0.87551913,
    ... 2.6514917, 2.01160156, 0.47699563]

    >>> def statistic(x): # permute only `x`
    ...     return stats.spearmanr(x, y).statistic
    >>> res_exact = stats.permutation_test((x,), statistic,
    ...     permutation_type='pairings')
    >>> res_asymptotic = stats.spearmanr(x, y)
    >>> res_exact.pvalue, res_asymptotic.pvalue # asymptotic pvalue is too low
    (0.10277777777777777, 0.07239650145772594)

    For a more detailed example, see :ref:`hypothesis_spearmanr`.
    """
    if axis is not None and axis > 1:
        raise ValueError("spearmanr only handles 1-D or 2-D arrays, "
                         f"supplied axis argument {axis}, please use only "
                         "values 0, 1 or None for axis")

    a, axisout = _chk_asarray(a, axis)
    if a.ndim > 2:
        raise ValueError("spearmanr only handles 1-D or 2-D arrays")

    if b is None:
        if a.ndim < 2:
            raise ValueError("`spearmanr` needs at least 2 "
                             "variables to compare")
    else:
        # Concatenate a and b, so that we now only have to handle the case
        # of a 2-D `a`.
        b, _ = _chk_asarray(b, axis)
        if axisout == 0:
            a = np.column_stack((a, b))
        else:
            a = np.vstack((a, b))

    n_vars = a.shape[1 - axisout]
    n_obs = a.shape[axisout]
    if n_obs <= 1:
        # Handle empty arrays or single observations.
        res = SignificanceResult(np.nan, np.nan)
        res.correlation = np.nan
        return res

    warn_msg = ("An input array is constant; the correlation coefficient "
                "is not defined.")

    constant_axis = False
    if axisout == 0:
        constant_columns = np.all(a == a[0, :], axis=0)
        constant_axis = np.any(constant_columns)
        if constant_axis:
            # If an input is constant, the correlation coefficient
            # is not defined.
            warnings.warn(stats.ConstantInputWarning(warn_msg), stacklevel=2)
    else:  # case when axisout == 1 b/c a is 2 dim only
        constant_rows = np.all(a.T == a.T[0, :], axis=0)
        constant_axis = np.any(constant_rows)
        if constant_axis:
            # If an input is constant, the correlation coefficient
            # is not defined.
            warnings.warn(stats.ConstantInputWarning(warn_msg), stacklevel=2)

    a_contains_nan = _contains_nan(a, nan_policy)
    variable_has_nan = np.zeros(n_vars, dtype=bool)
    if a_contains_nan:
        if nan_policy == 'omit':
            return mstats_basic.spearmanr(a, axis=axis, nan_policy=nan_policy,
                                          alternative=alternative)
        elif nan_policy == 'propagate':
            if a.ndim == 1 or n_vars <= 2:
                res = SignificanceResult(np.nan, np.nan)
                res.correlation = np.nan
                return res
            else:
                # Keep track of variables with NaNs, set the outputs to NaN
                # only for those variables
                variable_has_nan = np.isnan(a).any(axis=axisout)

    a_ranked = np.apply_along_axis(rankdata, axisout, a)

    if constant_axis:
        with np.errstate(invalid='ignore'):
            rs = np.corrcoef(a_ranked, rowvar=axisout)
    else:
        rs = np.corrcoef(a_ranked, rowvar=axisout)

    dof = n_obs - 2  # degrees of freedom

    # rs can have elements equal to 1, so avoid zero division warnings
    with np.errstate(divide='ignore'):
        # clip the small negative values possibly caused by rounding
        # errors before taking the square root
        t = rs * np.sqrt((dof/((rs+1.0)*(1.0-rs))).clip(0))

    dist = _SimpleStudentT(dof)
    prob = _get_pvalue(t, dist, alternative, xp=np)

    # For backwards compatibility, return scalars when comparing 2 columns
    if rs.shape == (2, 2):
        res = SignificanceResult(rs[1, 0], prob[1, 0])
        res.correlation = rs[1, 0]
        return res
    else:
        rs[variable_has_nan, :] = np.nan
        rs[:, variable_has_nan] = np.nan
        res = SignificanceResult(rs[()], prob[()])
        res.correlation = rs
        return res

