
def _kendalltau(x, y, *, method='auto', variant='b', alternative='two-sided'):
    x = np.asarray(x).ravel()
    y = np.asarray(y).ravel()

    if x.size != y.size:
        raise ValueError("Array shapes are incompatible for broadcasting.")
    elif not x.size or not y.size:
        # Return NaN if arrays are empty
        NaN = _get_nan(x, y)
        res = SignificanceResult(NaN, NaN)
        res.correlation = NaN
        return res

    def count_rank_tie(ranks):
        cnt = np.bincount(ranks).astype('int64', copy=False)
        cnt = cnt[cnt > 1]
        # Python ints to avoid overflow down the line
        return (int((cnt * (cnt - 1) // 2).sum()),
                int((cnt * (cnt - 1.) * (cnt - 2)).sum()),
                int((cnt * (cnt - 1.) * (2*cnt + 5)).sum()))

    size = x.size
    perm = np.argsort(y)  # sort on y and convert y to dense ranks
    x, y = x[perm], y[perm]
    y = np.r_[True, y[1:] != y[:-1]].cumsum(dtype=np.intp)

    # stable sort on x and convert x to dense ranks
    perm = np.argsort(x, kind='mergesort')
    x, y = x[perm], y[perm]
    x = np.r_[True, x[1:] != x[:-1]].cumsum(dtype=np.intp)

    dis = _kendall_dis(x, y)  # discordant pairs

    obs = np.r_[True, (x[1:] != x[:-1]) | (y[1:] != y[:-1]), True]
    cnt = np.diff(np.nonzero(obs)[0]).astype('int64', copy=False)

    ntie = int((cnt * (cnt - 1) // 2).sum())  # joint ties
    xtie, x0, x1 = count_rank_tie(x)     # ties in x, stats
    ytie, y0, y1 = count_rank_tie(y)     # ties in y, stats

    tot = (size * (size - 1)) // 2

    if xtie == tot or ytie == tot:
        NaN = _get_nan(x, y)
        res = SignificanceResult(NaN, NaN)
        res.correlation = NaN
        return res

    # Note that tot = con + dis + (xtie - ntie) + (ytie - ntie) + ntie
    #               = con + dis + xtie + ytie - ntie
    con_minus_dis = tot - xtie - ytie + ntie - 2 * dis
    if variant == 'b':
        tau = con_minus_dis / np.sqrt(tot - xtie) / np.sqrt(tot - ytie)
    elif variant == 'c':
        minclasses = min(len(set(x)), len(set(y)))
        tau = 2*con_minus_dis / (size**2 * (minclasses-1)/minclasses)
    else:
        raise ValueError(f"Unknown `variant` '{variant}' specified. "
                         "`variant` must be 'b' or 'c'.")

    # Limit range to fix computational errors
    tau = np.minimum(1., max(-1., tau))

    # The p-value calculation is the same for all variants since the p-value
    # depends only on con_minus_dis.
    if method == 'exact' and (xtie != 0 or ytie != 0):
        raise ValueError("Ties found; exact method cannot be used.")

    if method == 'auto':
        if (xtie == 0 and ytie == 0) and (size <= 33 or
                                          min(dis, tot-dis) <= 1):
            method = 'exact'
        else:
            method = 'asymptotic'

    if xtie == 0 and ytie == 0 and method == 'exact':
        pvalue = mstats_basic._kendall_p_exact(size, tot-dis, alternative)
    elif method == 'asymptotic':
        # con_minus_dis is approx normally distributed with this variance [3]_
        m = size * (size - 1.)
        var = ((m * (2*size + 5) - x1 - y1) / 18 +
               (2 * xtie * ytie) / m + x0 * y0 / (9 * m * (size - 2)))
        z = con_minus_dis / np.sqrt(var)
        pvalue = _get_pvalue(z, _SimpleNormal(), alternative, xp=np)
    else:
        raise ValueError(f"Unknown `method` '{method}' specified.  `method` must be"
                         "'auto', 'exact' or 'asymptotic'.")

    # create result object with alias for backward compatibility
    res = SignificanceResult(tau[()], pvalue[()])
    res.correlation = tau[()]
    return res

