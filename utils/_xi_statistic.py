
def _xi_statistic(x, y, y_continuous, xp):
    # Compute xi correlation statistic

    # `axis=-1` is guaranteed by _axis_nan_policy decorator
    n = x.shape[-1]

    # "Rearrange the data as (X(1), Y(1)), . . . ,(X(n), Y(n))
    # such that X(1) ≤ ··· ≤ X(n)"
    j = xp.argsort(x, axis=-1)
    j, y = xp.broadcast_arrays(j, y)
    y = xp.take_along_axis(y, j, axis=-1)

    # "Let ri be the rank of Y(i), that is, the number of j such that Y(j) ≤ Y(i)"
    r = stats.rankdata(y, method='max', axis=-1)
    # " additionally define li to be the number of j such that Y(j) ≥ Y(i)"
    # Could probably compute this from r, but that can be an enhancement
    l = stats.rankdata(-y, method='max', axis=-1)

    num = xp.sum(xp.abs(xp.diff(r, axis=-1)), axis=-1)
    if y_continuous:  # [1] Eq. 1.1
        statistic = 1 - 3 * num / (n ** 2 - 1)
    else:  # [1] Eq. 1.2
        den = 2 * xp.sum((n - l) * l, axis=-1)
        statistic = 1 - n * num / den

    return statistic, r, l

