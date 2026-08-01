
def alexandergovern(*samples, nan_policy='propagate', axis=0):
    """Performs the Alexander Govern test.

    The Alexander-Govern approximation tests the equality of k independent
    means in the face of heterogeneity of variance. The test is applied to
    samples from two or more groups, possibly with differing sizes.

    Parameters
    ----------
    *samples : array_like
        The sample measurements for each group.  There must be at least
        two samples, and each sample must contain at least two observations.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    Returns
    -------
    res : AlexanderGovernResult
        An object with attributes:

        statistic : float
            The computed A statistic of the test.
        pvalue : float
            The associated p-value from the chi-squared distribution.

    Warns
    -----
    `~scipy.stats.ConstantInputWarning`
        Raised if an input is a constant array.  The statistic is not defined
        in this case, so ``np.nan`` is returned.

    See Also
    --------
    f_oneway : one-way ANOVA

    Notes
    -----
    The use of this test relies on several assumptions.

    1. The samples are independent.
    2. Each sample is from a normally distributed population.
    3. Unlike `f_oneway`, this test does not assume on homoscedasticity,
       instead relaxing the assumption of equal variances.

    Input samples must be finite, one dimensional, and with size greater than
    one.

    References
    ----------
    .. [1] Alexander, Ralph A., and Diane M. Govern. "A New and Simpler
           Approximation for ANOVA under Variance Heterogeneity." Journal
           of Educational Statistics, vol. 19, no. 2, 1994, pp. 91-101.
           https://www.jstor.org/stable/1165140

    Examples
    --------
    >>> from scipy.stats import alexandergovern

    Here are some data on annual percentage rate of interest charged on
    new car loans at nine of the largest banks in four American cities
    taken from the National Institute of Standards and Technology's
    ANOVA dataset.

    We use `alexandergovern` to test the null hypothesis that all cities
    have the same mean APR against the alternative that the cities do not
    all have the same mean APR. We decide that a significance level of 5%
    is required to reject the null hypothesis in favor of the alternative.

    >>> atlanta = [13.75, 13.75, 13.5, 13.5, 13.0, 13.0, 13.0, 12.75, 12.5]
    >>> chicago = [14.25, 13.0, 12.75, 12.5, 12.5, 12.4, 12.3, 11.9, 11.9]
    >>> houston = [14.0, 14.0, 13.51, 13.5, 13.5, 13.25, 13.0, 12.5, 12.5]
    >>> memphis = [15.0, 14.0, 13.75, 13.59, 13.25, 12.97, 12.5, 12.25,
    ...           11.89]
    >>> alexandergovern(atlanta, chicago, houston, memphis)
    AlexanderGovernResult(statistic=4.65087071883494,
                          pvalue=0.19922132490385214)

    The p-value is 0.1992, indicating a nearly 20% chance of observing
    such an extreme value of the test statistic under the null hypothesis.
    This exceeds 5%, so we do not reject the null hypothesis in favor of
    the alternative.

    """
    xp = array_namespace(*samples)
    samples = _alexandergovern_input_validation(samples, nan_policy, axis, xp=xp)

    # The following formula numbers reference the equation described on
    # page 92 by Alexander, Govern. Formulas 5, 6, and 7 describe other
    # tests that serve as the basis for equation (8) but are not needed
    # to perform the test.

    # precalculate mean and length of each sample
    lengths = [_count_nonmasked(sample, axis=-1, xp=xp) for sample in samples]
    means = xp.stack([_xp_mean(sample, axis=-1) for sample in samples])

    # (1) determine standard error of the mean for each sample
    se2 = [(_xp_var(sample, correction=1, axis=-1) / length)
           for sample, length in zip(samples, lengths)]
    standard_errors_squared = xp.stack(se2)
    standard_errors = standard_errors_squared**0.5

    # Special case: statistic is NaN when variance is zero
    eps = xp.finfo(standard_errors.dtype).eps
    zero = standard_errors <= xp.abs(eps * means)
    NaN = xp.asarray(xp.nan, dtype=standard_errors.dtype)
    standard_errors = xp.where(zero, NaN, standard_errors)

    # (2) define a weight for each sample
    inv_sq_se = 1 / standard_errors_squared
    weights = inv_sq_se / xp.sum(inv_sq_se, axis=0, keepdims=True)

    # (3) determine variance-weighted estimate of the common mean
    # Consider replacing with vecdot when data-apis/array-api#910 is resolved
    var_w = xp.sum(weights * means, axis=0, keepdims=True)

    # (4) determine one-sample t statistic for each group
    t_stats = _demean(means, var_w, axis=0, xp=xp) / standard_errors

    # calculate parameters to be used in transformation
    if is_marray(xp):
        v = xp.stack(lengths) - 1
    else:
        v = xp.asarray(lengths, dtype=t_stats.dtype) - 1
        # align along 0th axis, which corresponds with separate samples
        v = xp.reshape(v, (-1,) + (1,)*(t_stats.ndim-1))
    a = v - .5
    b = 48 * a**2
    c = (a * xp.log(1 + (t_stats ** 2)/v))**.5

    # (8) perform a normalizing transformation on t statistic
    z = (c + ((c**3 + 3*c)/b) -
         ((4*c**7 + 33*c**5 + 240*c**3 + 855*c) /
          (b**2*10 + 8*b*c**4 + 1000*b)))

    # (9) calculate statistic
    A = xp.vecdot(z, z, axis=-z.ndim)
    A = A[()] if A.ndim == 0 else A  # data-apis/array-api-compat#355

    # "[the p value is determined from] central chi-square random deviates
    # with k - 1 degrees of freedom". Alexander, Govern (94)
    df = xp.asarray(len(samples) - 1, dtype=A.dtype)
    chi2 = _SimpleChi2(df)
    p = _get_pvalue(A, chi2, alternative='greater', symmetric=False, xp=xp)
    return AlexanderGovernResult(A, p)

