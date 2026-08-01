
def chi2_contingency(observed, correction=True, lambda_=None, *, method=None):
    """Chi-square test of independence of variables in a contingency table.

    This function computes the chi-square statistic and p-value for the
    hypothesis test of independence of the observed frequencies in the
    contingency table [1]_ `observed`.  The expected frequencies are computed
    based on the marginal sums under the assumption of independence; see
    `scipy.stats.contingency.expected_freq`.  The number of degrees of
    freedom is (expressed using numpy functions and attributes)::

        dof = observed.size - sum(observed.shape) + observed.ndim - 1


    Parameters
    ----------
    observed : array_like
        The contingency table. The table contains the observed frequencies
        (i.e. number of occurrences) in each category.  In the two-dimensional
        case, the table is often described as an "R x C table".
    correction : bool, optional
        If True, *and* the degrees of freedom is 1, apply Yates' correction
        for continuity.  The effect of the correction is to adjust each
        observed value by 0.5 towards the corresponding expected value.
    lambda_ : float or str, optional
        By default, the statistic computed in this test is Pearson's
        chi-squared statistic [2]_.  `lambda_` allows a statistic from the
        Cressie-Read power divergence family [3]_ to be used instead.  See
        `scipy.stats.power_divergence` for details.
    method : ResamplingMethod, optional
        Defines the method used to compute the p-value. Compatible only with
        ``correction=False``,  default `lambda_`, and two-way tables.
        If `method` is an instance of `scipy.stats.PermutationMethod` or
        `scipy.stats.MonteCarloMethod`, the p-value is computed using
        `scipy.stats.permutation_test`/`scipy.stats.monte_carlo_test` with the
        provided configuration options and other appropriate settings.
        Otherwise, the p-value is computed as documented in the notes.
        Note that if `method` is an instance of `scipy.stats.MonteCarloMethod`, the
        ``rvs`` attribute must be left unspecified; Monte Carlo samples are always drawn
        using the ``rvs`` method of `scipy.stats.random_table`.

        .. versionadded:: 1.15.0


    Returns
    -------
    res : Chi2ContingencyResult
        An object containing attributes:

        statistic : float
            The test statistic.
        pvalue : float
            The p-value of the test.
        dof : int
            The degrees of freedom. NaN if `method` is not ``None``.
        expected_freq : ndarray, same shape as `observed`
            The expected frequencies, based on the marginal sums of the table.

    See Also
    --------
    scipy.stats.contingency.expected_freq
    scipy.stats.fisher_exact
    scipy.stats.chisquare
    scipy.stats.power_divergence
    scipy.stats.barnard_exact
    scipy.stats.boschloo_exact
    :ref:`hypothesis_chi2_contingency` : Extended example

    Notes
    -----
    An often quoted guideline for the validity of this calculation is that
    the test should be used only if the observed and expected frequencies
    in each cell are at least 5.

    This is a test for the independence of different categories of a
    population. The test is only meaningful when the dimension of
    `observed` is two or more.  Applying the test to a one-dimensional
    table will always result in `expected` equal to `observed` and a
    chi-square statistic equal to 0.

    This function does not handle masked arrays, because the calculation
    does not make sense with missing values.

    Like `scipy.stats.chisquare`, this function computes a chi-square
    statistic; the convenience this function provides is to figure out the
    expected frequencies and degrees of freedom from the given contingency
    table. If these were already known, and if the Yates' correction was not
    required, one could use `scipy.stats.chisquare`.  That is, if one calls::

        res = chi2_contingency(obs, correction=False)

    then the following is true::

        (res.statistic, res.pvalue) == stats.chisquare(obs.ravel(),
                                                       f_exp=ex.ravel(),
                                                       ddof=obs.size - 1 - dof)

    The `lambda_` argument was added in version 0.13.0 of scipy.

    References
    ----------
    .. [1] "Contingency table",
           https://en.wikipedia.org/wiki/Contingency_table
    .. [2] "Pearson's chi-squared test",
           https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
    .. [3] Cressie, N. and Read, T. R. C., "Multinomial Goodness-of-Fit
           Tests", J. Royal Stat. Soc. Series B, Vol. 46, No. 3 (1984),
           pp. 440-464.

    Examples
    --------
    A two-way example (2 x 3):

    >>> import numpy as np
    >>> from scipy.stats import chi2_contingency
    >>> obs = np.array([[10, 10, 20], [20, 20, 20]])
    >>> res = chi2_contingency(obs)
    >>> res.statistic
    2.7777777777777777
    >>> res.pvalue
    0.24935220877729619
    >>> res.dof
    2
    >>> res.expected_freq
    array([[ 12.,  12.,  16.],
           [ 18.,  18.,  24.]])

    Perform the test using the log-likelihood ratio (i.e. the "G-test")
    instead of Pearson's chi-squared statistic.

    >>> res = chi2_contingency(obs, lambda_="log-likelihood")
    >>> res.statistic
    2.7688587616781319
    >>> res.pvalue
    0.25046668010954165

    A four-way example (2 x 2 x 2 x 2):

    >>> obs = np.array(
    ...     [[[[12, 17],
    ...        [11, 16]],
    ...       [[11, 12],
    ...        [15, 16]]],
    ...      [[[23, 15],
    ...        [30, 22]],
    ...       [[14, 17],
    ...        [15, 16]]]])
    >>> res = chi2_contingency(obs)
    >>> res.statistic
    8.7584514426741897
    >>> res.pvalue
    0.64417725029295503

    When the sum of the elements in a two-way table is small, the p-value
    produced by the default asymptotic approximation may be inaccurate.
    Consider passing a `PermutationMethod` or `MonteCarloMethod` as the
    `method` parameter with `correction=False`.

    >>> from scipy.stats import PermutationMethod
    >>> obs = np.asarray([[12, 3],
    ...                   [17, 16]])
    >>> res = chi2_contingency(obs, correction=False)
    >>> ref = chi2_contingency(obs, correction=False, method=PermutationMethod())
    >>> res.pvalue, ref.pvalue
    (0.0614122539870913, 0.1074)  # may vary

    For a more detailed example, see :ref:`hypothesis_chi2_contingency`.

    """
    observed = np.asarray(observed)
    if np.any(observed < 0):
        raise ValueError("All values in `observed` must be nonnegative.")
    if observed.size == 0:
        raise ValueError("No data; `observed` has size 0.")

    expected = expected_freq(observed)
    if np.any(expected == 0):
        # Include one of the positions where expected is zero in
        # the exception message.
        zeropos = list(zip(*np.nonzero(expected == 0)))[0]
        raise ValueError("The internally computed table of expected "
                         f"frequencies has a zero element at {zeropos}.")

    if method is not None:
        return _chi2_resampling_methods(observed, expected, correction, lambda_, method)

    # The degrees of freedom
    dof = expected.size - sum(expected.shape) + expected.ndim - 1

    if dof == 0:
        # Degenerate case; this occurs when `observed` is 1D (or, more
        # generally, when it has only one nontrivial dimension).  In this
        # case, we also have observed == expected, so chi2 is 0.
        chi2 = 0.0
        p = 1.0
    else:
        if dof == 1 and correction:
            # Adjust `observed` according to Yates' correction for continuity.
            # Magnitude of correction no bigger than difference; see gh-13875
            diff = expected - observed
            direction = np.sign(diff)
            magnitude = np.minimum(0.5, np.abs(diff))
            observed = observed + magnitude * direction

        chi2, p = power_divergence(observed, expected,
                                   ddof=observed.size - 1 - dof, axis=None,
                                   lambda_=lambda_)

    return Chi2ContingencyResult(chi2, p, dof, expected)

