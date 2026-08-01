
def pearsonr(x, y):
    r"""
    Pearson correlation coefficient and p-value for testing non-correlation.

    The Pearson correlation coefficient [1]_ measures the linear relationship
    between two datasets.  The calculation of the p-value relies on the
    assumption that each dataset is normally distributed.  (See Kowalski [3]_
    for a discussion of the effects of non-normality of the input on the
    distribution of the correlation coefficient.)  Like other correlation
    coefficients, this one varies between -1 and +1 with 0 implying no
    correlation. Correlations of -1 or +1 imply an exact linear relationship.

    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.

    Returns
    -------
    r : float
        Pearson's correlation coefficient.
    p-value : float
        Two-tailed p-value.

    Warns
    -----
    `~scipy.stats.ConstantInputWarning`
        Raised if an input is a constant array.  The correlation coefficient
        is not defined in this case, so ``np.nan`` is returned.

    `~scipy.stats.NearConstantInputWarning`
        Raised if an input is "nearly" constant.  The array ``x`` is considered
        nearly constant if ``norm(x - mean(x)) < 1e-13 * abs(mean(x))``.
        Numerical errors in the calculation ``x - mean(x)`` in this case might
        result in an inaccurate calculation of r.

    See Also
    --------
    spearmanr : Spearman rank-order correlation coefficient.
    kendalltau : Kendall's tau, a correlation measure for ordinal data.

    Notes
    -----
    The correlation coefficient is calculated as follows:

    .. math::

        r = \frac{\sum (x - m_x) (y - m_y)}
                 {\sqrt{\sum (x - m_x)^2 \sum (y - m_y)^2}}

    where :math:`m_x` is the mean of the vector x and :math:`m_y` is
    the mean of the vector y.

    Under the assumption that x and y are drawn from
    independent normal distributions (so the population correlation coefficient
    is 0), the probability density function of the sample correlation
    coefficient r is ([1]_, [2]_):

    .. math::

        f(r) = \frac{{(1-r^2)}^{n/2-2}}{\mathrm{B}(\frac{1}{2},\frac{n}{2}-1)}

    where n is the number of samples, and B is the beta function.  This
    is sometimes referred to as the exact distribution of r.  This is
    the distribution that is used in `pearsonr` to compute the p-value.
    The distribution is a beta distribution on the interval [-1, 1],
    with equal shape parameters a = b = n/2 - 1.  In terms of SciPy's
    implementation of the beta distribution, the distribution of r is::

        dist = scipy.stats.beta(n/2 - 1, n/2 - 1, loc=-1, scale=2)

    The p-value returned by `pearsonr` is a two-sided p-value. The p-value
    roughly indicates the probability of an uncorrelated system
    producing datasets that have a Pearson correlation at least as extreme
    as the one computed from these datasets. More precisely, for a
    given sample with correlation coefficient r, the p-value is
    the probability that abs(r') of a random sample x' and y' drawn from
    the population with zero correlation would be greater than or equal
    to abs(r). In terms of the object ``dist`` shown above, the p-value
    for a given r and length n can be computed as::

        p = 2*dist.cdf(-abs(r))

    When n is 2, the above continuous distribution is not well-defined.
    One can interpret the limit of the beta distribution as the shape
    parameters a and b approach a = b = 0 as a discrete distribution with
    equal probability masses at r = 1 and r = -1.  More directly, one
    can observe that, given the data x = [x1, x2] and y = [y1, y2], and
    assuming x1 != x2 and y1 != y2, the only possible values for r are 1
    and -1.  Because abs(r') for any sample x' and y' with length 2 will
    be 1, the two-sided p-value for a sample of length 2 is always 1.

    References
    ----------
    .. [1] "Pearson correlation coefficient", Wikipedia,
           https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    .. [2] Student, "Probable error of a correlation coefficient",
           Biometrika, Volume 6, Issue 2-3, 1 September 1908, pp. 302-310.
    .. [3] C. J. Kowalski, "On the Effects of Non-Normality on the Distribution
           of the Sample Product-Moment Correlation Coefficient"
           Journal of the Royal Statistical Society. Series C (Applied
           Statistics), Vol. 21, No. 1 (1972), pp. 1-12.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> from scipy.stats import mstats
    >>> mstats.pearsonr([1, 2, 3, 4, 5], [10, 9, 2.5, 6, 4])
    (-0.7426106572325057, 0.1505558088534455)

    There is a linear dependence between x and y if y = a + b*x + e, where
    a,b are constants and e is a random error term, assumed to be independent
    of x. For simplicity, assume that x is standard normal, a=0, b=1 and let
    e follow a normal distribution with mean zero and standard deviation s>0.

    >>> s = 0.5
    >>> x = stats.norm.rvs(size=500)
    >>> e = stats.norm.rvs(scale=s, size=500)
    >>> y = x + e
    >>> mstats.pearsonr(x, y)
    (0.9029601878969703, 8.428978827629898e-185) # may vary

    This should be close to the exact value given by

    >>> 1/np.sqrt(1 + s**2)
    0.8944271909999159

    For s=0.5, we observe a high level of correlation. In general, a large
    variance of the noise reduces the correlation, while the correlation
    approaches one as the variance of the error goes to zero.

    It is important to keep in mind that no correlation does not imply
    independence unless (x, y) is jointly normal. Correlation can even be zero
    when there is a very simple dependence structure: if X follows a
    standard normal distribution, let y = abs(x). Note that the correlation
    between x and y is zero. Indeed, since the expectation of x is zero,
    cov(x, y) = E[x*y]. By definition, this equals E[x*abs(x)] which is zero
    by symmetry. The following lines of code illustrate this observation:

    >>> y = np.abs(x)
    >>> mstats.pearsonr(x, y)
    (-0.016172891856853524, 0.7182823678751942) # may vary

    A non-zero correlation coefficient can be misleading. For example, if X has
    a standard normal distribution, define y = x if x < 0 and y = 0 otherwise.
    A simple calculation shows that corr(x, y) = sqrt(2/Pi) = 0.797...,
    implying a high level of correlation:

    >>> y = np.where(x < 0, x, 0)
    >>> mstats.pearsonr(x, y)
    (0.8537091583771509, 3.183461621422181e-143) # may vary

    This is unintuitive since there is no dependence of x and y if x is larger
    than zero which happens in about half of the cases if we sample x and y.
    """
    (x, y, n) = _chk_size(x, y)
    (x, y) = (x.ravel(), y.ravel())
    # Get the common mask and the total nb of unmasked elements
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    n -= m.sum()
    df = n-2
    if df < 0:
        return (masked, masked)

    return scipy.stats._stats_py.pearsonr(
                ma.masked_array(x, mask=m).compressed(),
                ma.masked_array(y, mask=m).compressed())


def pearsonr(x, y, *, alternative='two-sided', method=None, axis=0):
    r"""
    Pearson correlation coefficient and p-value for testing non-correlation.

    The Pearson correlation coefficient [1]_ measures the linear relationship
    between two datasets. Like other correlation
    coefficients, this one varies between -1 and +1 with 0 implying no
    correlation. Correlations of -1 or +1 imply an exact linear relationship.
    Positive correlations imply that as x increases, so does y. Negative
    correlations imply that as x increases, y decreases.

    This function also performs a test of the null hypothesis that the
    distributions underlying the samples are uncorrelated and normally
    distributed. (See Kowalski [3]_
    for a discussion of the effects of non-normality of the input on the
    distribution of the correlation coefficient.)
    The p-value roughly indicates the probability of an uncorrelated system
    producing datasets that have a Pearson correlation at least as extreme
    as the one computed from these datasets.

    Parameters
    ----------
    x : array_like
        Input array.
    y : array_like
        Input array.
    alternative : {'two-sided', 'greater', 'less'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the correlation is nonzero
        * 'less': the correlation is negative (less than zero)
        * 'greater':  the correlation is positive (greater than zero)

        .. versionadded:: 1.9.0
    method : ResamplingMethod, optional
        Defines the method used to compute the p-value. If `method` is an
        instance of `PermutationMethod`/`MonteCarloMethod`, the p-value is
        computed using
        `scipy.stats.permutation_test`/`scipy.stats.monte_carlo_test` with the
        provided configuration options and other appropriate settings.
        Otherwise, the p-value is computed as documented in the notes.

        .. versionadded:: 1.11.0
    axis : int or None, default
        Axis along which to perform the calculation. Default is 0.
        If None, ravel both arrays before performing the calculation.

        .. versionadded:: 1.14.0

    Returns
    -------
    result : `~scipy.stats._result_classes.PearsonRResult`
        An object with the following attributes:

        statistic : float
            Pearson product-moment correlation coefficient.
        pvalue : float
            The p-value associated with the chosen alternative.

        The object has the following method:

        confidence_interval(confidence_level, method)
            This computes the confidence interval of the correlation
            coefficient `statistic` for the given confidence level.
            The confidence interval is returned in a ``namedtuple`` with
            fields `low` and `high`. If `method` is not provided, the
            confidence interval is computed using the Fisher transformation
            [1]_. If `method` is an instance of `BootstrapMethod`, the
            confidence interval is computed using `scipy.stats.bootstrap` with
            the provided configuration options and other appropriate settings.
            In some cases, confidence limits may be NaN due to a degenerate
            resample, and this is typical for very small samples (~6
            observations).

    Raises
    ------
    ValueError
        If `x` and `y` do not have length at least 2.

    Warns
    -----
    `~scipy.stats.ConstantInputWarning`
        Raised if an input is a constant array.  The correlation coefficient
        is not defined in this case, so ``np.nan`` is returned.

    `~scipy.stats.NearConstantInputWarning`
        Raised if an input is "nearly" constant.  The array ``x`` is considered
        nearly constant if ``norm(x - mean(x)) < 1e-13 * abs(mean(x))``.
        Numerical errors in the calculation ``x - mean(x)`` in this case might
        result in an inaccurate calculation of r.

    See Also
    --------
    spearmanr : Spearman rank-order correlation coefficient.
    kendalltau : Kendall's tau, a correlation measure for ordinal data.
    :ref:`hypothesis_pearsonr` : Extended example

    Notes
    -----
    The correlation coefficient is calculated as follows:

    .. math::

        r = \frac{\sum (x - m_x) (y - m_y)}
                 {\sqrt{\sum (x - m_x)^2 \sum (y - m_y)^2}}

    where :math:`m_x` is the mean of the vector x and :math:`m_y` is
    the mean of the vector y.

    Under the assumption that x and y are drawn from
    independent normal distributions (so the population correlation coefficient
    is 0), the probability density function of the sample correlation
    coefficient r is ([1]_, [2]_):

    .. math::
        f(r) = \frac{{(1-r^2)}^{n/2-2}}{\mathrm{B}(\frac{1}{2},\frac{n}{2}-1)}

    where n is the number of samples, and B is the beta function.  This
    is sometimes referred to as the exact distribution of r.  This is
    the distribution that is used in `pearsonr` to compute the p-value when
    the `method` parameter is left at its default value (None).
    The distribution is a beta distribution on the interval [-1, 1],
    with equal shape parameters a = b = n/2 - 1.  In terms of SciPy's
    implementation of the beta distribution, the distribution of r is::

        dist = scipy.stats.beta(n/2 - 1, n/2 - 1, loc=-1, scale=2)

    The default p-value returned by `pearsonr` is a two-sided p-value. For a
    given sample with correlation coefficient r, the p-value is
    the probability that abs(r') of a random sample x' and y' drawn from
    the population with zero correlation would be greater than or equal
    to abs(r). In terms of the object ``dist`` shown above, the p-value
    for a given r and length n can be computed as::

        p = 2*dist.cdf(-abs(r))

    When n is 2, the above continuous distribution is not well-defined.
    One can interpret the limit of the beta distribution as the shape
    parameters a and b approach a = b = 0 as a discrete distribution with
    equal probability masses at r = 1 and r = -1.  More directly, one
    can observe that, given the data x = [x1, x2] and y = [y1, y2], and
    assuming x1 != x2 and y1 != y2, the only possible values for r are 1
    and -1.  Because abs(r') for any sample x' and y' with length 2 will
    be 1, the two-sided p-value for a sample of length 2 is always 1.

    For backwards compatibility, the object that is returned also behaves
    like a tuple of length two that holds the statistic and the p-value.

    References
    ----------
    .. [1] "Pearson correlation coefficient", Wikipedia,
           https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    .. [2] Student, "Probable error of a correlation coefficient",
           Biometrika, Volume 6, Issue 2-3, 1 September 1908, pp. 302-310.
    .. [3] C. J. Kowalski, "On the Effects of Non-Normality on the Distribution
           of the Sample Product-Moment Correlation Coefficient"
           Journal of the Royal Statistical Society. Series C (Applied
           Statistics), Vol. 21, No. 1 (1972), pp. 1-12.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> x, y = [1, 2, 3, 4, 5, 6, 7], [10, 9, 2.5, 6, 4, 3, 2]
    >>> res = stats.pearsonr(x, y)
    >>> res
    PearsonRResult(statistic=-0.828503883588428, pvalue=0.021280260007523286)

    To perform an exact permutation version of the test:

    >>> rng = np.random.default_rng(7796654889291491997)
    >>> method = stats.PermutationMethod(n_resamples=np.inf, random_state=rng)
    >>> stats.pearsonr(x, y, method=method)
    PearsonRResult(statistic=-0.828503883588428, pvalue=0.028174603174603175)

    To perform the test under the null hypothesis that the data were drawn from
    *uniform* distributions:

    >>> method = stats.MonteCarloMethod(rvs=(rng.uniform, rng.uniform))
    >>> stats.pearsonr(x, y, method=method)
    PearsonRResult(statistic=-0.828503883588428, pvalue=0.0188)

    To produce an asymptotic 90% confidence interval:

    >>> res.confidence_interval(confidence_level=0.9)
    ConfidenceInterval(low=-0.9644331982722841, high=-0.3460237473272273)

    And for a bootstrap confidence interval:

    >>> method = stats.BootstrapMethod(method='BCa', rng=rng)
    >>> res.confidence_interval(confidence_level=0.9, method=method)
    ConfidenceInterval(low=-0.9983163756488651, high=-0.22771001702132443)  # may vary

    If N-dimensional arrays are provided, multiple tests are performed in a
    single call according to the same conventions as most `scipy.stats` functions:

    >>> rng = np.random.default_rng(2348246935601934321)
    >>> x = rng.standard_normal((8, 15))
    >>> y = rng.standard_normal((8, 15))
    >>> stats.pearsonr(x, y, axis=0).statistic.shape  # between corresponding columns
    (15,)
    >>> stats.pearsonr(x, y, axis=1).statistic.shape  # between corresponding rows
    (8,)

    To perform all pairwise comparisons between slices of the arrays,
    use standard NumPy broadcasting techniques. For instance, to compute the
    correlation between all pairs of rows:

    >>> stats.pearsonr(x[:, np.newaxis, :], y, axis=-1).statistic.shape
    (8, 8)

    There is a linear dependence between x and y if y = a + b*x + e, where
    a,b are constants and e is a random error term, assumed to be independent
    of x. For simplicity, assume that x is standard normal, a=0, b=1 and let
    e follow a normal distribution with mean zero and standard deviation s>0.

    >>> rng = np.random.default_rng()
    >>> s = 0.5
    >>> x = stats.norm.rvs(size=500, random_state=rng)
    >>> e = stats.norm.rvs(scale=s, size=500, random_state=rng)
    >>> y = x + e
    >>> stats.pearsonr(x, y).statistic
    0.9001942438244763

    This should be close to the exact value given by

    >>> 1/np.sqrt(1 + s**2)
    0.8944271909999159

    For s=0.5, we observe a high level of correlation. In general, a large
    variance of the noise reduces the correlation, while the correlation
    approaches one as the variance of the error goes to zero.

    It is important to keep in mind that no correlation does not imply
    independence unless (x, y) is jointly normal. Correlation can even be zero
    when there is a very simple dependence structure: if X follows a
    standard normal distribution, let y = abs(x). Note that the correlation
    between x and y is zero. Indeed, since the expectation of x is zero,
    cov(x, y) = E[x*y]. By definition, this equals E[x*abs(x)] which is zero
    by symmetry. The following lines of code illustrate this observation:

    >>> y = np.abs(x)
    >>> stats.pearsonr(x, y)
    PearsonRResult(statistic=-0.05444919272687482, pvalue=0.22422294836207743)

    A non-zero correlation coefficient can be misleading. For example, if X has
    a standard normal distribution, define y = x if x < 0 and y = 0 otherwise.
    A simple calculation shows that corr(x, y) = sqrt(2/Pi) = 0.797...,
    implying a high level of correlation:

    >>> y = np.where(x < 0, x, 0)
    >>> stats.pearsonr(x, y)
    PearsonRResult(statistic=0.861985781588, pvalue=4.813432002751103e-149)

    This is unintuitive since there is no dependence of x and y if x is larger
    than zero which happens in about half of the cases if we sample x and y.

    For a more detailed example, see :ref:`hypothesis_pearsonr`.

    """
    xp = array_namespace(x, y)
    x, y = xp_promote(x, y, force_floating=True, xp=xp)
    dtype = x.dtype

    if not is_numpy(xp) and method is not None:
        method = 'invalid'

    if axis is None:
        x = xp.reshape(x, (-1,))
        y = xp.reshape(y, (-1,))
        axis = -1

    axis_int = int(axis)
    if axis_int != axis:
        raise ValueError('`axis` must be an integer.')
    axis = axis_int

    try:
        np.broadcast_shapes(x.shape, y.shape)
        # For consistency with other `stats` functions, we need to
        # match the dimensionalities before looking at `axis`.
        # (Note: this is not the NEP 5 / gufunc order of operations;
        #  see TestPearsonr::test_different_dimensionality for more information.)
        ndim = max(x.ndim, y.ndim)
        x = xp.reshape(x, (1,) * (ndim - x.ndim) + x.shape)
        y = xp.reshape(y, (1,) * (ndim - y.ndim) + y.shape)

    except (ValueError, RuntimeError) as e:
        message = '`x` and `y` must be broadcastable.'
        raise ValueError(message) from e

    if x.shape[axis] != y.shape[axis]:
        raise ValueError('`x` and `y` must have the same length along `axis`.')

    if x.shape[axis] < 2:
        raise ValueError('`x` and `y` must have length at least 2.')

    x, y = _share_masks(x, y, xp=xp)
    n = xp.asarray(_count_nonmasked(x, axis=axis), dtype=x.dtype)

    x = xp.moveaxis(x, axis, -1)
    y = xp.moveaxis(y, axis, -1)
    axis = -1

    if xp.isdtype(dtype, "complex floating"):
        raise ValueError('This function does not support complex data')

    x = xp.astype(x, dtype, copy=False)
    y = xp.astype(y, dtype, copy=False)
    threshold = xp.finfo(dtype).eps ** 0.75

    # If an input is constant, the correlation coefficient is not defined.
    if is_marray(xp):
        # sort to ensure that we are comparing to a non-masked element
        const_x = xp.all(x == xp.sort(x, axis=-1)[..., 0:1], axis=-1)
        const_y = xp.all(y == xp.sort(y, axis=-1)[..., 0:1], axis=-1)
    else:
        const_x = xp.all(x == x[..., 0:1], axis=-1)
        const_y = xp.all(y == y[..., 0:1], axis=-1)
    const_xy = const_x | const_y

    any_const_xy = xp.any(const_xy)
    lazy = is_lazy_array(const_xy)
    if not lazy and any_const_xy:
        msg = ("An input array is constant; the correlation coefficient "
               "is not defined.")
        warnings.warn(stats.ConstantInputWarning(msg), stacklevel=2)
    if lazy or any_const_xy:
        x = xp.where(const_x[..., xp.newaxis], xp.nan, x)
        y = xp.where(const_y[..., xp.newaxis], xp.nan, y)

    if isinstance(method, PermutationMethod):
        def statistic(y, axis):
            statistic, _ = pearsonr(x, y, axis=axis, alternative=alternative)
            return statistic

        res = permutation_test((y,), statistic, permutation_type='pairings',
                               axis=axis, alternative=alternative, **method._asdict())

        return PearsonRResult(statistic=res.statistic, pvalue=res.pvalue, n=n,
                              alternative=alternative, x=x, y=y, axis=axis)
    elif isinstance(method, MonteCarloMethod):
        def statistic(x, y, axis):
            statistic, _ = pearsonr(x, y, axis=axis, alternative=alternative)
            return statistic

        # `monte_carlo_test` accepts an `rvs` tuple of callables, not an `rng`
        # If the user specified an `rng`, replace it with the appropriate callables
        method = method._asdict()
        if (rng := method.pop('rng', None)) is not None:  # goo-goo g'joob
            rng = np.random.default_rng(rng)
            method['rvs'] = rng.normal, rng.normal

        res = monte_carlo_test((x, y,), statistic=statistic, axis=axis,
                               alternative=alternative, **method)

        return PearsonRResult(statistic=res.statistic, pvalue=res.pvalue, n=n,
                              alternative=alternative, x=x, y=y, axis=axis)
    elif method == 'invalid':
        message = '`method` must be `None` if arguments are not NumPy arrays.'
        raise ValueError(message)
    elif method is not None:
        message = ('`method` must be an instance of `PermutationMethod`, '
                   '`MonteCarloMethod`, or None.')
        raise ValueError(message)

    xmean = xp.mean(x, axis=axis, keepdims=True)
    ymean = xp.mean(y, axis=axis, keepdims=True)
    xm = x - xmean
    ym = y - ymean

    # scipy.linalg.norm(xm) avoids premature overflow when xm is e.g.
    # [-5e210, 5e210, 3e200, -3e200]
    # but not when `axis` is provided, so scale manually. scipy.linalg.norm
    # also raises an error with NaN input rather than returning NaN, so
    # use np.linalg.norm.
    xmax = xp.max(xp.abs(xm), axis=axis, keepdims=True)
    ymax = xp.max(xp.abs(ym), axis=axis, keepdims=True)
    with np.errstate(invalid='ignore', divide='ignore'):
        normxm = xmax * xp_vector_norm(xm/xmax, axis=axis, keepdims=True)
        normym = ymax * xp_vector_norm(ym/ymax, axis=axis, keepdims=True)

    if not lazy:
        nconst_x = xp.any(normxm < threshold*xp.abs(xmean), axis=axis)
        nconst_y = xp.any(normym < threshold*xp.abs(ymean), axis=axis)
        nconst_xy = nconst_x | nconst_y
        if xp.any(nconst_xy & (~const_xy)):
            # If all the values in x (likewise y) are very close to the mean,
            # the loss of precision that occurs in the subtraction xm = x - xmean
            # might result in large errors in r.
            msg = ("An input array is nearly constant; the computed "
                "correlation coefficient may be inaccurate.")
            warnings.warn(stats.NearConstantInputWarning(msg), stacklevel=2)

    with np.errstate(invalid='ignore', divide='ignore'):
        r = xp.vecdot(xm / normxm, ym / normym, axis=axis)

    # Presumably, if abs(r) > 1, then it is only some small artifact of
    # floating point arithmetic.
    r = xp.clip(r, -1., 1.)
    r = xpx.at(r, const_xy).set(xp.nan)

    # As explained in the docstring, the distribution of `r` under the null
    # hypothesis is the beta distribution on (-1, 1) with a = b = n/2 - 1.
    ab = xp.asarray(n/2 - 1, dtype=dtype, device=xp_device(x))
    dist = _SimpleBeta(ab, ab, loc=-1, scale=2)
    pvalue = _get_pvalue(r, dist, alternative, xp=xp)

    mask = (n == 2)   #  return exactly 1.0 or -1.0 values for n == 2 case as promised
    # data-apis/array-api-extra#196
    mxp = array_namespace(r._meta) if is_dask(xp) else xp
    def special_case(r):
        return mxp.where(mxp.isnan(r), mxp.nan, mxp.ones_like(r))
    r = xpx.apply_where(mask, r, mxp.round, fill_value=r)
    pvalue = xpx.apply_where(mask, (r,), special_case, fill_value=pvalue)

    r = r[()] if r.ndim == 0 else r
    pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue
    return PearsonRResult(statistic=r, pvalue=pvalue, n=n,
                          alternative=alternative, x=x, y=y, axis=axis)

