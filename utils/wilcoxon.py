
def wilcoxon(x, y=None, zero_method="wilcox", correction=False,
             alternative="two-sided", method='auto', *, axis=0):
    """Calculate the Wilcoxon signed-rank test.

    The Wilcoxon signed-rank test tests the null hypothesis that two
    related paired samples come from the same distribution. In particular,
    it tests whether the distribution of the differences ``x - y`` is symmetric
    about zero. It is a non-parametric version of the paired T-test.

    Parameters
    ----------
    x : array_like
        Either the first set of measurements (in which case ``y`` is the second
        set of measurements), or the differences between two sets of
        measurements (in which case ``y`` is not to be specified.)  Must be
        one-dimensional.
    y : array_like, optional
        Either the second set of measurements (if ``x`` is the first set of
        measurements), or not specified (if ``x`` is the differences between
        two sets of measurements.)  Must be one-dimensional.

        .. warning::
            When `y` is provided, `wilcoxon` calculates the test statistic
            based on the ranks of the absolute values of ``d = x - y``.
            Roundoff error in the subtraction can result in elements of ``d``
            being assigned different ranks even when they would be tied with
            exact arithmetic. Rather than passing `x` and `y` separately,
            consider computing the difference ``x - y``, rounding as needed to
            ensure that only truly unique elements are numerically distinct,
            and passing the result as `x`, leaving `y` at the default (None).

    zero_method : {"wilcox", "pratt", "zsplit"}, optional
        There are different conventions for handling pairs of observations
        with equal values ("zero-differences", or "zeros").

        * "wilcox": Discards all zero-differences (default); see [4]_.
        * "pratt": Includes zero-differences in the ranking process,
          but drops the ranks of the zeros (more conservative); see [3]_.
          In this case, the normal approximation is adjusted as in [5]_.
        * "zsplit": Includes zero-differences in the ranking process and
          splits the zero rank between positive and negative ones.

    correction : bool, optional
        If True, apply continuity correction by adjusting the Wilcoxon rank
        statistic by 0.5 towards the mean value when computing the
        z-statistic if a normal approximation is used.  Default is False.
    alternative : {"two-sided", "greater", "less"}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        In the following, let ``d`` represent the difference between the paired
        samples: ``d = x - y`` if both ``x`` and ``y`` are provided, or
        ``d = x`` otherwise.

        * 'two-sided': the distribution underlying ``d`` is not symmetric
          about zero.
        * 'less': the distribution underlying ``d`` is stochastically less
          than a distribution symmetric about zero.
        * 'greater': the distribution underlying ``d`` is stochastically
          greater than a distribution symmetric about zero.

    method : {"auto", "exact", "asymptotic"} or `PermutationMethod` instance, optional
        Method to calculate the p-value, see Notes. Default is "auto".

    axis : int or None, default: 0
        If an int, the axis of the input along which to compute the statistic.
        The statistic of each axis-slice (e.g. row) of the input will appear
        in a corresponding element of the output. If ``None``, the input will
        be raveled before computing the statistic.

    Returns
    -------
    result : WilcoxonResult
        An object with the following attributes.

        statistic : array_like
            If `alternative` is "two-sided", the sum of the ranks of the
            differences above or below zero, whichever is smaller.
            Otherwise the sum of the ranks of the differences above zero.
        pvalue : array_like
            The p-value for the test depending on `alternative` and `method`.
        zstatistic : array_like
            When ``method = 'asymptotic'``, this is the normalized z-statistic::

                z = (T - mn - d) / se

            where ``T`` is `statistic` as defined above, ``mn`` is the mean of the
            distribution under the null hypothesis, ``d`` is a continuity
            correction, and ``se`` is the standard error.
            When ``method != 'asymptotic'``, this attribute is not available.

    See Also
    --------
    kruskal, mannwhitneyu

    Notes
    -----
    In the following, let ``d`` represent the difference between the paired
    samples: ``d = x - y`` if both ``x`` and ``y`` are provided, or ``d = x``
    otherwise. Assume that all elements of ``d`` are independent and
    identically distributed observations, and all are distinct and nonzero.

    - When ``len(d)`` is sufficiently large, the null distribution of the
      normalized test statistic (`zstatistic` above) is approximately normal,
      and ``method = 'asymptotic'`` can be used to compute the p-value.
    - When ``len(d)`` is small, the normal approximation may not be accurate,
      and ``method='exact'`` is preferred (at the cost of additional
      execution time).
    - The default, ``method='auto'``, selects between the two:
      ``method='exact'`` is used when ``len(d) <= 50``, and
      ``method='asymptotic'`` is used otherwise.

    The presence of "ties" (i.e. not all elements of ``d`` are unique) or
    "zeros" (i.e. elements of ``d`` are zero) changes the null distribution
    of the test statistic, and ``method='exact'`` no longer calculates
    the exact p-value. If ``method='asymptotic'``, the z-statistic is adjusted
    for more accurate comparison against the standard normal, but still,
    for finite sample sizes, the standard normal is only an approximation of
    the true null distribution of the z-statistic. For such situations, the
    `method` parameter also accepts instances of `PermutationMethod`. In this
    case, the p-value is computed using `permutation_test` with the provided
    configuration options and other appropriate settings.

    The presence of ties and zeros affects the resolution of ``method='auto'``
    accordingly: exhasutive permutations are performed when ``len(d) <= 13``,
    and the asymptotic method is used otherwise. Note that they asymptotic
    method may not be very accurate even for ``len(d) > 14``; the threshold
    was chosen as a compromise between execution time and accuracy under the
    constraint that the results must be deterministic. Consider providing an
    instance of `PermutationMethod` method manually, choosing the
    ``n_resamples`` parameter to balance time constraints and accuracy
    requirements.

    Please also note that in the edge case that all elements of ``d`` are zero,
    the p-value relying on the normal approximaton cannot be computed (NaN)
    if ``zero_method='wilcox'`` or ``zero_method='pratt'``.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test
    .. [2] Conover, W.J., Practical Nonparametric Statistics, 1971.
    .. [3] Pratt, J.W., Remarks on Zeros and Ties in the Wilcoxon Signed
       Rank Procedures, Journal of the American Statistical Association,
       Vol. 54, 1959, pp. 655-667. :doi:`10.1080/01621459.1959.10501526`
    .. [4] Wilcoxon, F., Individual Comparisons by Ranking Methods,
       Biometrics Bulletin, Vol. 1, 1945, pp. 80-83. :doi:`10.2307/3001968`
    .. [5] Cureton, E.E., The Normal Approximation to the Signed-Rank
       Sampling Distribution When Zero Differences are Present,
       Journal of the American Statistical Association, Vol. 62, 1967,
       pp. 1068-1069. :doi:`10.1080/01621459.1967.10500917`

    Examples
    --------
    In [4]_, the differences in height between cross- and self-fertilized
    corn plants is given as follows:

    >>> d = [6, 8, 14, 16, 23, 24, 28, 29, 41, -48, 49, 56, 60, -67, 75]

    Cross-fertilized plants appear to be higher. To test the null
    hypothesis that there is no height difference, we can apply the
    two-sided test:

    >>> from scipy.stats import wilcoxon
    >>> res = wilcoxon(d)
    >>> res.statistic, res.pvalue
    (24.0, 0.041259765625)

    Hence, we would reject the null hypothesis at a confidence level of 5%,
    concluding that there is a difference in height between the groups.
    To confirm that the median of the differences can be assumed to be
    positive, we use:

    >>> res = wilcoxon(d, alternative='greater')
    >>> res.statistic, res.pvalue
    (96.0, 0.0206298828125)

    This shows that the null hypothesis that the median is negative can be
    rejected at a confidence level of 5% in favor of the alternative that
    the median is greater than zero. The p-values above are exact. Using the
    normal approximation gives very similar values:

    >>> res = wilcoxon(d, method='asymptotic')
    >>> res.statistic, res.pvalue
    (24.0, 0.04088813291185591)

    Note that the statistic changed to 96 in the one-sided case (the sum
    of ranks of positive differences) whereas it is 24 in the two-sided
    case (the minimum of sum of ranks above and below zero).

    In the example above, the differences in height between paired plants are
    provided to `wilcoxon` directly. Alternatively, `wilcoxon` accepts two
    samples of equal length, calculates the differences between paired
    elements, then performs the test. Consider the samples ``x`` and ``y``:

    >>> import numpy as np
    >>> x = np.array([0.5, 0.825, 0.375, 0.5])
    >>> y = np.array([0.525, 0.775, 0.325, 0.55])
    >>> res = wilcoxon(x, y, alternative='greater')
    >>> res
    WilcoxonResult(statistic=5.0, pvalue=0.5625)

    Note that had we calculated the differences by hand, the test would have
    produced different results:

    >>> d = [-0.025, 0.05, 0.05, -0.05]
    >>> ref = wilcoxon(d, alternative='greater')
    >>> ref
    WilcoxonResult(statistic=6.0, pvalue=0.5)

    The substantial difference is due to roundoff error in the results of
    ``x-y``:

    >>> d - (x-y)
    array([2.08166817e-17, 6.93889390e-17, 1.38777878e-17, 4.16333634e-17])

    Even though we expected all the elements of ``(x-y)[1:]`` to have the same
    magnitude ``0.05``, they have slightly different magnitudes in practice,
    and therefore are assigned different ranks in the test. Before performing
    the test, consider calculating ``d`` and adjusting it as necessary to
    ensure that theoretically identically values are not numerically distinct.
    For example:

    >>> d2 = np.around(x - y, decimals=3)
    >>> wilcoxon(d2, alternative='greater')
    WilcoxonResult(statistic=6.0, pvalue=0.5)

    """
    # replace approx by asymptotic to ensure backwards compatability
    if method == "approx":
        method = "asymptotic"
    return _wilcoxon._wilcoxon_nd(x, y, zero_method, correction, alternative,
                                  method, axis)

