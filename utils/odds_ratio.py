
def odds_ratio(table, *, kind='conditional'):
    r"""
    Compute the odds ratio for a 2x2 contingency table.

    Parameters
    ----------
    table : array_like of ints
        A 2x2 contingency table.  Elements must be non-negative integers.
    kind : str, optional
        Which kind of odds ratio to compute, either the sample
        odds ratio (``kind='sample'``) or the conditional odds ratio
        (``kind='conditional'``).  Default is ``'conditional'``.

    Returns
    -------
    result : `~scipy.stats._result_classes.OddsRatioResult` instance
        The returned object has two computed attributes:

        statistic : float
            * If `kind` is ``'sample'``, this is sample (or unconditional)
              estimate, given by
              ``table[0, 0]*table[1, 1]/(table[0, 1]*table[1, 0])``.
            * If `kind` is ``'conditional'``, this is the conditional
              maximum likelihood estimate for the odds ratio. It is
              the noncentrality parameter of Fisher's noncentral
              hypergeometric distribution with the same hypergeometric
              parameters as `table` and whose mean is ``table[0, 0]``.

        The object has the method `confidence_interval` that computes
        the confidence interval of the odds ratio.

    See Also
    --------
    scipy.stats.fisher_exact
    relative_risk
    :ref:`hypothesis_odds_ratio` : Extended example

    Notes
    -----
    The conditional odds ratio was discussed by Fisher (see "Example 1"
    of [1]_).  Texts that cover the odds ratio include [2]_ and [3]_.

    .. versionadded:: 1.10.0

    References
    ----------
    .. [1] R. A. Fisher (1935), The logic of inductive inference,
           Journal of the Royal Statistical Society, Vol. 98, No. 1,
           pp. 39-82.
    .. [2] Breslow NE, Day NE (1980). Statistical methods in cancer research.
           Volume I - The analysis of case-control studies. IARC Sci Publ.
           (32):5-338. PMID: 7216345. (See section 4.2.)
    .. [3] H. Sahai and A. Khurshid (1996), Statistics in Epidemiology:
           Methods, Techniques, and Applications, CRC Press LLC, Boca
           Raton, Florida.

    Examples
    --------
    In epidemiology, individuals are classified as "exposed" or
    "unexposed" to some factor or treatment. If the occurrence of some
    illness is under study, those who have the illness are often
    classified as "cases", and those without it are "noncases".  The
    counts of the occurrences of these classes gives a contingency
    table::

                    exposed    unexposed
        cases          a           b
        noncases       c           d

    The sample odds ratio may be written ``(a/c) / (b/d)``.  ``a/c`` can
    be interpreted as the odds of a case occurring in the exposed group,
    and ``b/d`` as the odds of a case occurring in the unexposed group.
    The sample odds ratio is the ratio of these odds.  If the odds ratio
    is greater than 1, it suggests that there is a positive association
    between being exposed and being a case.

    Interchanging the rows or columns of the contingency table inverts
    the odds ratio, so it is important to understand the meaning of labels
    given to the rows and columns of the table when interpreting the
    odds ratio.

    Consider a hypothetical example where it is hypothesized that exposure to a
    certain chemical is associated with increased occurrence of a certain
    disease. Suppose we have the following table for a collection of 410 people::

                exposed unexposed
        cases        7       15
        noncases    58      472

    The question we ask is "Is exposure to the chemical associated with
    increased risk of the disease?"

    Compute the odds ratio:

    >>> from scipy.stats.contingency import odds_ratio
    >>> res = odds_ratio([[7, 15], [58, 472]])
    >>> res.statistic
    3.7836687705553493

    For this sample, the odds of getting the disease for those who have been
    exposed to the chemical are almost 3.8 times that of those who have not been
    exposed.

    We can compute the 95% confidence interval for the odds ratio:

    >>> res.confidence_interval(confidence_level=0.95)
    ConfidenceInterval(low=1.2514829132266785, high=10.363493716701269)

    The 95% confidence interval for the conditional odds ratio is approximately
    (1.25, 10.4).

    For a more detailed example, see :ref:`hypothesis_odds_ratio`.
    """
    if kind not in ['conditional', 'sample']:
        raise ValueError("`kind` must be 'conditional' or 'sample'.")

    c = np.asarray(table)

    if c.shape != (2, 2):
        raise ValueError(f"Invalid shape {c.shape}. The input `table` must be "
                         "of shape (2, 2).")

    if not np.issubdtype(c.dtype, np.integer):
        raise ValueError("`table` must be an array of integers, but got "
                         f"type {c.dtype}")
    c = c.astype(np.int64)

    if np.any(c < 0):
        raise ValueError("All values in `table` must be nonnegative.")

    if 0 in c.sum(axis=0) or 0 in c.sum(axis=1):
        # If both values in a row or column are zero, the p-value is NaN and
        # the odds ratio is NaN.
        result = OddsRatioResult(_table=c, _kind=kind, statistic=np.nan)
        return result

    if kind == 'sample':
        oddsratio = _sample_odds_ratio(c)
    else:  # kind is 'conditional'
        oddsratio = _conditional_oddsratio(c)

    result = OddsRatioResult(_table=c, _kind=kind, statistic=oddsratio)
    return result

