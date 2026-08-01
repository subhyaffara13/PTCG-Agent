
def f_oneway(*args):
    """
    Performs a 1-way ANOVA, returning an F-value and probability given
    any number of groups.  From Heiman, pp.394-7.

    Usage: ``f_oneway(*args)``, where ``*args`` is 2 or more arrays,
    one per treatment group.

    Returns
    -------
    statistic : float
        The computed F-value of the test.
    pvalue : float
        The associated p-value from the F-distribution.

    """
    # Construct a single array of arguments: each row is a group
    data = argstoarray(*args)
    ngroups = len(data)
    ntot = data.count()
    sstot = (data**2).sum() - (data.sum())**2/float(ntot)
    ssbg = (data.count(-1) * (data.mean(-1)-data.mean())**2).sum()
    sswg = sstot-ssbg
    dfbg = ngroups-1
    dfwg = ntot - ngroups
    msb = ssbg/float(dfbg)
    msw = sswg/float(dfwg)
    f = msb/msw
    prob = special.fdtrc(dfbg, dfwg, f)  # equivalent to stats.f.sf

    return F_onewayResult(f, prob)


def f_oneway(*samples, axis=0, equal_var=True):
    """Perform one-way ANOVA.

    The one-way ANOVA tests the null hypothesis that two or more groups have
    the same population mean.  The test is applied to samples from two or
    more groups, possibly with differing sizes.

    Parameters
    ----------
    *samples : array_like
        The sample measurements for each group.  There must be at least
        two arguments.  If the arrays are multidimensional, then all the
        dimensions of the array must be the same except for `axis`.
    axis : int, optional
        Axis of the input arrays along which the test is applied.
        Default is 0.
    equal_var : bool, optional
        If True (default), perform a standard one-way ANOVA test that
        assumes equal population variances [2]_.
        If False, perform Welch's ANOVA test, which does not assume
        equal population variances [4]_.

        .. versionadded:: 1.16.0

    Returns
    -------
    statistic : float
        The computed F statistic of the test.
    pvalue : float
        The associated p-value from the F distribution.

    Warns
    -----
    `~scipy.stats.ConstantInputWarning`
        Emitted if all values within each of the input arrays are identical.
        In this case the F statistic is either infinite or isn't defined,
        so ``np.inf`` or ``np.nan`` is returned.

    RuntimeWarning
        Emitted if the length of any input array is 0, or if all the input
        arrays have length 1.  ``np.nan`` is returned for the F statistic
        and the p-value in these cases.

    Notes
    -----
    The ANOVA test has important assumptions that must be satisfied in order
    for the associated p-value to be valid.

    1. The samples are independent.
    2. Each sample is from a normally distributed population.
    3. The population standard deviations of the groups are all equal.  This
       property is known as homoscedasticity.

    If these assumptions are not true for a given set of data, it may still
    be possible to use the Kruskal-Wallis H-test (`scipy.stats.kruskal`) or
    the Alexander-Govern test (`scipy.stats.alexandergovern`) although with
    some loss of power.

    The length of each group must be at least one, and there must be at
    least one group with length greater than one.  If these conditions
    are not satisfied, a warning is generated and (``np.nan``, ``np.nan``)
    is returned.

    If all values in each group are identical, and there exist at least two
    groups with different values, the function generates a warning and
    returns (``np.inf``, 0).

    If all values in all groups are the same, function generates a warning
    and returns (``np.nan``, ``np.nan``).

    The algorithm is from Heiman [2]_, pp.394-7.

    References
    ----------
    .. [1] R. Lowry, "Concepts and Applications of Inferential Statistics",
           Chapter 14, 2014, http://vassarstats.net/textbook/

    .. [2] G.W. Heiman, "Understanding research methods and statistics: An
           integrated introduction for psychology", Houghton, Mifflin and
           Company, 2001.

    .. [3] J.H. McDonald, "Handbook of Biological Statistics",
           One-way ANOVA, 2014.
           http://www.biostathandbook.com/onewayanova.html

    .. [4] B. L. Welch, "On the Comparison of Several Mean Values:
           An Alternative Approach", Biometrika, vol. 38, no. 3/4,
           pp. 330-336, 1951. :doi:`10.2307/2332579`.

    .. [5] J.H. McDonald, R. Seed and R.K. Koehn, "Allozymes and
           morphometric characters of three species of Mytilus in
           the Northern and Southern Hemispheres",
           Marine Biology, vol. 111, pp. 323-333, 1991.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import f_oneway

    Here are some data [3]_ on a shell measurement (the length of the anterior
    adductor muscle scar, standardized by dividing by length) in the mussel
    Mytilus trossulus from five locations: Tillamook, Oregon; Newport, Oregon;
    Petersburg, Alaska; Magadan, Russia; and Tvarminne, Finland, taken from a
    much larger data set used in [5]_.

    >>> tillamook = [0.0571, 0.0813, 0.0831, 0.0976, 0.0817, 0.0859, 0.0735,
    ...              0.0659, 0.0923, 0.0836]
    >>> newport = [0.0873, 0.0662, 0.0672, 0.0819, 0.0749, 0.0649, 0.0835,
    ...            0.0725]
    >>> petersburg = [0.0974, 0.1352, 0.0817, 0.1016, 0.0968, 0.1064, 0.105]
    >>> magadan = [0.1033, 0.0915, 0.0781, 0.0685, 0.0677, 0.0697, 0.0764,
    ...            0.0689]
    >>> tvarminne = [0.0703, 0.1026, 0.0956, 0.0973, 0.1039, 0.1045]
    >>> f_oneway(tillamook, newport, petersburg, magadan, tvarminne)
    F_onewayResult(statistic=7.121019471642447, pvalue=0.0002812242314534544)

    `f_oneway` accepts multidimensional input arrays.  When the inputs
    are multidimensional and `axis` is not given, the test is performed
    along the first axis of the input arrays.  For the following data, the
    test is performed three times, once for each column.

    >>> a = np.array([[9.87, 9.03, 6.81],
    ...               [7.18, 8.35, 7.00],
    ...               [8.39, 7.58, 7.68],
    ...               [7.45, 6.33, 9.35],
    ...               [6.41, 7.10, 9.33],
    ...               [8.00, 8.24, 8.44]])
    >>> b = np.array([[6.35, 7.30, 7.16],
    ...               [6.65, 6.68, 7.63],
    ...               [5.72, 7.73, 6.72],
    ...               [7.01, 9.19, 7.41],
    ...               [7.75, 7.87, 8.30],
    ...               [6.90, 7.97, 6.97]])
    >>> c = np.array([[3.31, 8.77, 1.01],
    ...               [8.25, 3.24, 3.62],
    ...               [6.32, 8.81, 5.19],
    ...               [7.48, 8.83, 8.91],
    ...               [8.59, 6.01, 6.07],
    ...               [3.07, 9.72, 7.48]])
    >>> F = f_oneway(a, b, c)
    >>> F.statistic
    array([1.75676344, 0.03701228, 3.76439349])
    >>> F.pvalue
    array([0.20630784, 0.96375203, 0.04733157])

    Welch ANOVA will be performed if `equal_var` is False.

    """
    xp = array_namespace(*samples)
    samples = xp_promote(*samples, force_floating=True, xp=xp)

    if len(samples) < 2:
        raise TypeError('at least two inputs are required;'
                        f' got {len(samples)}.')

    # ANOVA on N groups, each in its own array
    num_groups = len(samples)

    # axis is guaranteed to be -1 by the _axis_nan_policy decorator
    alldata = xp.concat(samples, axis=-1)
    bign = _count_nonmasked(alldata, axis=-1, xp=xp)

    # Check if the inputs are too small (for testing _axis_nan_policy decorator)
    if _f_oneway_is_too_small(samples):
        NaN = _get_nan(*samples, xp=xp)
        return F_onewayResult(NaN, NaN)

    # Check if all values within each group are identical, and if the common
    # value in at least one group is different from that in another group.
    # Based on https://github.com/scipy/scipy/issues/11669

    # If axis=0, say, and the groups have shape (n0, ...), (n1, ...), ...,
    # then is_const is a boolean array with shape (num_groups, ...).
    # It is True if the values within the groups along the axis slice are
    # identical. In the typical case where each input array is 1-d, is_const is
    # a 1-d array with length num_groups.
    is_const = xp.concat([xp.all(xp.diff(sample, axis=-1) == 0, axis=-1, keepdims=True)
                          for sample in samples], axis=-1)

    # all_const is a boolean array with shape (...) (see previous comment).
    # It is True if the values within each group along the axis slice are
    # the same (e.g. [[3, 3, 3], [5, 5, 5, 5], [4, 4, 4]]).
    all_const = xp.all(is_const, axis=-1)

    # all_same_const is True if all the values in the groups along the axis=0
    # slice are the same (e.g. [[3, 3, 3], [3, 3, 3, 3], [3, 3, 3]]).
    all_same_const = xp.all(xp.diff(alldata, axis=-1) == 0, axis=-1)

    if not isinstance(equal_var, bool):
        raise TypeError("Expected a boolean value for 'equal_var'")

    if equal_var:
        # Determine the mean of the data, and subtract that from all inputs to a
        # variance (via sum_of_sq / sq_of_sum) calculation.  Variance is invariant
        # to a shift in location, and centering all data around zero vastly
        # improves numerical stability.
        offset = xp.mean(alldata, axis=-1, keepdims=True)
        alldata = alldata - offset

        normalized_ss = xp.sum(alldata, axis=-1)**2. / bign

        sstot = xp.vecdot(alldata, alldata, axis=-1) - normalized_ss

        ssbn = 0
        for sample in samples:
            smo_ss = xp.sum(sample - offset, axis=-1)**2.
            ssbn = ssbn + smo_ss / _count_nonmasked(sample, axis=-1, xp=xp)

        # Naming: variables ending in bn/b are for "between treatments", wn/w are
        # for "within treatments"
        ssbn = ssbn - normalized_ss
        sswn = sstot - ssbn
        dfbn = num_groups - 1
        dfwn = bign - num_groups
        msb = ssbn / dfbn
        msw = sswn / dfwn
        with np.errstate(divide='ignore', invalid='ignore'):
            f = msb / msw
        dfn, dfd = dfbn, dfwn

    else:
        # calculate basic statistics for each sample
        # Beginning of second paragraph [4] page 1:
        # "As a particular case $y_t$ may be the means ... of samples
        y_t = xp.stack([xp.mean(sample, axis=-1) for sample in samples])
        # "... of $n_t$ observations..."
        if is_marray(xp):
            n_t = xp.stack([_count_nonmasked(sample, axis=-1, xp=xp)
                            for sample in samples])
            n_t = xp.asarray(n_t, dtype=n_t.dtype)
        else:
            n_t = xp.asarray([sample.shape[-1] for sample in samples], dtype=y_t.dtype)
            n_t = xp.reshape(n_t, (-1,) + (1,) * (y_t.ndim - 1))
        # "... from $k$ different normal populations..."
        k = len(samples)
        # "The separate samples provide estimates $s_t^2$ of the $\sigma_t^2$."
        s_t2 = xp.stack([xp.var(sample, axis=-1, correction=1) for sample in samples])

        # calculate weight by number of data and variance
        # "we have $\lambda_t = 1 / n_t$ ... where w_t = 1 / {\lambda_t s_t^2}$"
        w_t = n_t / s_t2
        # sum of w_t
        s_w_t = xp.sum(w_t, axis=0)

        # calculate adjusted grand mean
        # "... and $\hat{y} = \sum w_t y_t / \sum w_t$. When all..."
        axis_zero = -w_t.ndim
        y_hat = xp.vecdot(w_t, y_t, axis=axis_zero) / xp.sum(w_t, axis=0)

        # adjust f statistic
        # ref.[4] p.334 eq.29
        numerator =  xp.vecdot(w_t, (y_t - y_hat)**2, axis=axis_zero) / (k - 1)
        denominator = (
                1 + 2 * (k - 2) / (k**2 - 1) *
                xp.vecdot(1 / (n_t - 1), (1 - w_t / s_w_t)**2, axis=axis_zero)
        )
        f = numerator / denominator

        # degree of freedom 1
        # ref.[4] p.334 eq.30
        hat_f1 = k - 1

        # adjusted degree of freedom 2
        # ref.[4] p.334 eq.30
        hat_f2 = (
                (k**2 - 1) /
                (3 * xp.vecdot(1 / (n_t - 1), (1 - w_t / s_w_t)**2, axis=axis_zero))
        )

        dfn, dfd = hat_f1, hat_f2

    # Fix any f values that should be inf or nan because the corresponding
    # inputs were constant.
    f = xpx.at(f)[all_const].set(xp.inf)
    f = xpx.at(f)[all_same_const].set(xp.nan)

    # calculate p value
    # ref.[4] p.334 eq.28
    prob = special.fdtrc(dfn, dfd, f)

    f, prob = (f[()], prob[()]) if f.ndim == 0 else (f, prob)
    return F_onewayResult(f, prob)

