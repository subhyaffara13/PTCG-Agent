
def kendalltau(x, y, use_ties=True, use_missing=False, method='auto',
               alternative='two-sided'):
    """
    Computes Kendall's rank correlation tau on two variables *x* and *y*.

    Parameters
    ----------
    x : sequence
        First data list (for example, time).
    y : sequence
        Second data list.
    use_ties : {True, False}, optional
        Whether ties correction should be performed.
    use_missing : {False, True}, optional
        Whether missing data should be allocated a rank of 0 (False) or the
        average rank (True)
    method : {'auto', 'asymptotic', 'exact'}, optional
        Defines which method is used to calculate the p-value [1]_.
        'asymptotic' uses a normal approximation valid for large samples.
        'exact' computes the exact p-value, but can only be used if no ties
        are present. As the sample size increases, the 'exact' computation
        time may grow and the result may lose some precision.
        'auto' is the default and selects the appropriate
        method based on a trade-off between speed and accuracy.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the rank correlation is nonzero
        * 'less': the rank correlation is negative (less than zero)
        * 'greater':  the rank correlation is positive (greater than zero)

    Returns
    -------
    res : SignificanceResult
        An object containing attributes:

        statistic : float
           The tau statistic.
        pvalue : float
           The p-value for a hypothesis test whose null hypothesis is
           an absence of association, tau = 0.

    References
    ----------
    .. [1] Maurice G. Kendall, "Rank Correlation Methods" (4th Edition),
           Charles Griffin & Co., 1970.

    """
    (x, y, n) = _chk_size(x, y)
    (x, y) = (x.flatten(), y.flatten())
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    if m is not nomask:
        x = ma.array(x, mask=m, copy=True)
        y = ma.array(y, mask=m, copy=True)
        # need int() here, otherwise numpy defaults to 32 bit
        # integer on all Windows architectures, causing overflow.
        # int() will keep it infinite precision.
        n -= int(m.sum())

    if n < 2:
        res = scipy.stats._stats_py.SignificanceResult(np.nan, np.nan)
        res.correlation = np.nan
        return res

    rx = ma.masked_equal(rankdata(x, use_missing=use_missing), 0)
    ry = ma.masked_equal(rankdata(y, use_missing=use_missing), 0)
    idx = rx.argsort()
    (rx, ry) = (rx[idx], ry[idx])
    C = np.sum([((ry[i+1:] > ry[i]) * (rx[i+1:] > rx[i])).filled(0).sum()
                for i in range(len(ry)-1)], dtype=float)
    D = np.sum([((ry[i+1:] < ry[i])*(rx[i+1:] > rx[i])).filled(0).sum()
                for i in range(len(ry)-1)], dtype=float)
    xties = count_tied_groups(x)
    yties = count_tied_groups(y)
    if use_ties:
        corr_x = np.sum([v*k*(k-1) for (k,v) in xties.items()], dtype=float)
        corr_y = np.sum([v*k*(k-1) for (k,v) in yties.items()], dtype=float)
        denom = ma.sqrt((n*(n-1)-corr_x)/2. * (n*(n-1)-corr_y)/2.)
    else:
        denom = n*(n-1)/2.
    tau = (C-D) / denom

    if method == 'exact' and (xties or yties):
        raise ValueError("Ties found, exact method cannot be used.")

    if method == 'auto':
        if (not xties and not yties) and (n <= 33 or min(C, n*(n-1)/2.0-C) <= 1):
            method = 'exact'
        else:
            method = 'asymptotic'

    if not xties and not yties and method == 'exact':
        prob = _kendall_p_exact(n, C, alternative)

    elif method == 'asymptotic':
        var_s = n*(n-1)*(2*n+5)
        if use_ties:
            var_s -= np.sum([v*k*(k-1)*(2*k+5)*1. for (k,v) in xties.items()])
            var_s -= np.sum([v*k*(k-1)*(2*k+5)*1. for (k,v) in yties.items()])
            v1 = (np.sum([v*k*(k-1) for (k, v) in xties.items()], dtype=float) *
                  np.sum([v*k*(k-1) for (k, v) in yties.items()], dtype=float))
            v1 /= 2.*n*(n-1)
            if n > 2:
                v2 = np.sum([v*k*(k-1)*(k-2) for (k,v) in xties.items()],
                            dtype=float) * \
                     np.sum([v*k*(k-1)*(k-2) for (k,v) in yties.items()],
                            dtype=float)
                v2 /= 9.*n*(n-1)*(n-2)
            else:
                v2 = 0
        else:
            v1 = v2 = 0

        var_s /= 18.
        var_s += (v1 + v2)
        z = (C-D)/np.sqrt(var_s)
        prob = scipy.stats._stats_py._get_pvalue(z, distributions.norm, alternative)
    else:
        raise ValueError("Unknown method "+str(method)+" specified, please "
                         "use auto, exact or asymptotic.")

    res = scipy.stats._stats_py.SignificanceResult(tau[()], prob[()])
    res.correlation = tau
    return res


def kendalltau(x, y, *, nan_policy='propagate', method='auto', variant='b',
               alternative='two-sided', axis=None, keepdims=False):
    r"""Calculate Kendall's tau, a correlation measure for ordinal data.

    Kendall's tau is a measure of the correspondence between two rankings.
    Values close to 1 indicate strong agreement, and values close to -1
    indicate strong disagreement. This implements two variants of Kendall's
    tau: tau-b (the default) and tau-c (also known as Stuart's tau-c). These
    differ only in how they are normalized to lie within the range -1 to 1;
    the hypothesis tests (their p-values) are identical. Kendall's original
    tau-a is not implemented separately because both tau-b and tau-c reduce
    to tau-a in the absence of ties.

    Although a naive implementation has O(n^2) complexity, this implementation
    uses a Fenwick tree to do the computation in O(n log(n)) complexity.

    Parameters
    ----------
    x, y : array_like
        Arrays of rankings, of the same shape. If arrays are not 1-D, they
        will be flattened to 1-D.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    method : {'auto', 'asymptotic', 'exact'}, optional
        Defines which method is used to calculate the p-value [5]_.
        The following options are available (default is 'auto'):

        * 'auto': selects the appropriate method based on a trade-off
          between speed and accuracy
        * 'asymptotic': uses a normal approximation valid for large samples
        * 'exact': computes the exact p-value, but can only be used if no ties
          are present. As the sample size increases, the 'exact' computation
          time may grow and the result may lose some precision.

    variant : {'b', 'c'}, optional
        Defines which variant of Kendall's tau is returned. Default is 'b'.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the rank correlation is nonzero
        * 'less': the rank correlation is negative (less than zero)
        * 'greater': the rank correlation is positive (greater than zero)
    axis : int or None, default: None
        If an int, the axis of the input along which to compute the statistic.
        The statistic of each axis-slice (e.g. row) of the input will appear in a
        corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.
    keepdims : bool, optional
        If this is set to ``True``, the axes which are reduced are left
        in the result as dimensions with length one. With this option,
        the result will broadcast correctly against the input array.

    Returns
    -------
    res : SignificanceResult
        An object containing attributes:

        statistic : float
           The tau statistic.
        pvalue : float
           The p-value for a hypothesis test whose null hypothesis is
           an absence of association, tau = 0.

    Raises
    ------
    ValueError
        If `nan_policy` is 'omit' and `variant` is not 'b' or
        if `method` is 'exact' and there are ties between `x` and `y`.

    See Also
    --------
    spearmanr : Calculates a Spearman rank-order correlation coefficient.
    theilslopes : Computes the Theil-Sen estimator for a set of points (x, y).
    weightedtau : Computes a weighted version of Kendall's tau.
    :ref:`hypothesis_kendalltau` : Extended example

    Notes
    -----
    The definition of Kendall's tau that is used is [2]_::

      tau_b = (P - Q) / sqrt((P + Q + T) * (P + Q + U))

      tau_c = 2 (P - Q) / (n**2 * (m - 1) / m)

    where P is the number of concordant pairs, Q the number of discordant
    pairs, T the number of tied pairs only in `x`, and U the number of tied pairs only
    in `y`.  If a tie occurs for the same pair in both `x` and `y`, it is not
    added to either T or U. n is the total number of samples, and m is the
    number of unique values in either `x` or `y`, whichever is smaller.

    References
    ----------
    .. [1] Maurice G. Kendall, "A New Measure of Rank Correlation", Biometrika
           Vol. 30, No. 1/2, pp. 81-93, 1938.
    .. [2] Maurice G. Kendall, "The treatment of ties in ranking problems",
           Biometrika Vol. 33, No. 3, pp. 239-251. 1945.
    .. [3] Gottfried E. Noether, "Elements of Nonparametric Statistics", John
           Wiley & Sons, 1967.
    .. [4] Peter M. Fenwick, "A new data structure for cumulative frequency
           tables", Software: Practice and Experience, Vol. 24, No. 3,
           pp. 327-336, 1994.
    .. [5] Maurice G. Kendall, "Rank Correlation Methods" (4th Edition),
           Charles Griffin & Co., 1970.

    Examples
    --------

    >>> from scipy import stats
    >>> x1 = [12, 2, 1, 12, 2]
    >>> x2 = [1, 4, 7, 1, 0]
    >>> res = stats.kendalltau(x1, x2)
    >>> res.statistic
    -0.47140452079103173
    >>> res.pvalue
    0.2827454599327748

    For a more detailed example, see :ref:`hypothesis_kendalltau`.
    """
    xp = array_namespace(x, y)
    x, y = xp_promote(x, y, force_floating=True, xp=xp)
    dtype = x.dtype
    if is_marray(xp):
        mask_x, mask_y = np.asarray(x.mask), np.asarray(y.mask)
        x, y = np.asarray(x.data).copy(), np.asarray(y.data).copy()
        unmasked_nans = np.any(np.isnan(x[~mask_x])) | np.any(np.isnan(y[~mask_y]))
        if unmasked_nans:
            if nan_policy == 'propagate':
                message = "`nan_policy='propagate'` is incompatible with MArray input."
            elif nan_policy == 'raise':
                message = "The input contains nan values."
            raise ValueError(message)
        nan_policy = 'omit'
        x[mask_x], y[mask_y] = np.nan, np.nan
    else:
        x, y = _asarray(x, subok=True, xp=np), _asarray(y, subok=True, xp=np)
    res = _kendalltau(x, y, nan_policy=nan_policy, method=method, variant=variant,
                      alternative=alternative, axis=axis, keepdims=keepdims)
    vals = res.statistic, res.pvalue, res.statistic
    vals = (xp.asarray(val, dtype=dtype)[()] if val.ndim == 0
            else xp.asarray(val, dtype=dtype) for val in vals)
    return _pack_CorrelationResult(*vals)


def kendalltau(*args, _no_deco=False, **kwargs):
    if _no_deco:
        return stats._stats_py._kendalltau(*args, _no_deco=_no_deco, **kwargs)
    return stats.kendalltau(*args, **kwargs)

