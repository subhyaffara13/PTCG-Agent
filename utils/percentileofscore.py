
def percentileofscore(a, score, kind='rank', nan_policy='propagate'):
    """Compute the percentile rank of a score relative to a list of scores.

    A `percentileofscore` of, for example, 80% means that 80% of the
    scores in `a` are below the given score. In the case of gaps or
    ties, the exact definition depends on the optional keyword, `kind`.

    Parameters
    ----------
    a : array_like
        A 1-D array to which `score` is compared.
    score : float or array_like
        A float score or array of scores for which to compute the percentile(s).
    kind : {'rank', 'weak', 'strict', 'mean'}, optional
        Specifies the interpretation of the resulting score.
        The following options are available (default is 'rank'):

        * 'rank': Average percentage ranking of score.  In case of multiple
          matches, average the percentage rankings of all matching scores.
        * 'weak': This kind corresponds to the definition of a cumulative
          distribution function.  A percentileofscore of 80% means that 80%
          of values are less than or equal to the provided score.
        * 'strict': Similar to "weak", except that only values that are
          strictly less than the given score are counted.
        * 'mean': The average of the "weak" and "strict" scores, often used
          in testing.  See https://en.wikipedia.org/wiki/Percentile_rank

    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Specifies how to treat `nan` values in `a`.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan (for each value in `score`).
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    Returns
    -------
    pcos : float or array-like
        Percentile-position(s) of `score` (0-100) relative to `a`.

    See Also
    --------
    numpy.percentile
    scipy.stats.scoreatpercentile, scipy.stats.rankdata

    Examples
    --------
    Three-quarters of the given values lie below a given score:

    >>> import numpy as np
    >>> from scipy import stats
    >>> stats.percentileofscore([1, 2, 3, 4], 3)
    75.0

    With multiple matches, note how the scores of the two matches, 0.6
    and 0.8 respectively, are averaged:

    >>> stats.percentileofscore([1, 2, 3, 3, 4], 3)
    70.0

    Only 2/5 values are strictly less than 3:

    >>> stats.percentileofscore([1, 2, 3, 3, 4], 3, kind='strict')
    40.0

    But 4/5 values are less than or equal to 3:

    >>> stats.percentileofscore([1, 2, 3, 3, 4], 3, kind='weak')
    80.0

    The average between the weak and the strict scores is:

    >>> stats.percentileofscore([1, 2, 3, 3, 4], 3, kind='mean')
    60.0

    Score arrays (of any dimensionality) are supported:

    >>> stats.percentileofscore([1, 2, 3, 3, 4], [2, 3])
    array([40., 70.])

    The inputs can be infinite:

    >>> stats.percentileofscore([-np.inf, 0, 1, np.inf], [1, 2, np.inf])
    array([75., 75., 100.])

    If `a` is empty, then the resulting percentiles are all `nan`:

    >>> stats.percentileofscore([], [1, 2])
    array([nan, nan])
    """

    a = np.asarray(a)
    score = np.asarray(score)

    if a.ndim != 1:
        raise ValueError("`a` must be 1-dimensional.")

    n = len(a)

    # Nan treatment
    cna = _contains_nan(a, nan_policy)
    cns = _contains_nan(score, nan_policy)

    if cns:
        # If a score is nan, then the output should be nan
        # (also if nan_policy is "omit", because it only applies to `a`)
        score = ma.masked_where(np.isnan(score), score)

    if cna:
        if nan_policy == "omit":
            # Don't count nans
            a = ma.masked_where(np.isnan(a), a)
            n = a.count()

        if nan_policy == "propagate":
            # All outputs should be nans
            n = 0

    # Cannot compare to empty list ==> nan
    if n == 0:
        perct = np.full_like(score, np.nan, dtype=np.float64)

    else:
        # Prepare broadcasting
        score = score[..., None]

        def count(x):
            return np.count_nonzero(x, -1)

        # Main computations/logic
        if kind == 'rank':
            left = count(a < score)
            right = count(a <= score)
            plus1 = left < right
            perct = (left + right + plus1) * (50.0 / n)
        elif kind == 'strict':
            perct = count(a < score) * (100.0 / n)
        elif kind == 'weak':
            perct = count(a <= score) * (100.0 / n)
        elif kind == 'mean':
            left = count(a < score)
            right = count(a <= score)
            perct = (left + right) * (50.0 / n)
        else:
            raise ValueError(
                "kind can only be 'rank', 'strict', 'weak' or 'mean'")

    # Re-insert nan values
    perct = ma.filled(perct, np.nan)

    if perct.ndim == 0:
        return perct[()]
    return perct

