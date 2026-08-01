
def _bws_statistic(x, y, alternative, axis, xp):
    '''Compute the BWS test statistic for two independent samples'''
    # Public function currently does not accept `axis`, but `permutation_test`
    # uses `axis` to make vectorized call.

    Ri, Hj = xp.sort(x, axis=axis), xp.sort(y, axis=axis)
    n, m = Ri.shape[axis], Hj.shape[axis]
    i, j = xp.arange(1, n+1, dtype=Ri.dtype), xp.arange(1, m+1, dtype=Hj.dtype)

    Bx_num = Ri - (m + n)/n * i
    By_num = Hj - (m + n)/m * j

    if alternative == 'two-sided':
        Bx_num = xpx.at(Bx_num)[...].multiply(Bx_num)
        By_num = xpx.at(By_num)[...].multiply(By_num)
    else:
        Bx_num = xpx.at(Bx_num)[...].multiply(xp.abs(Bx_num))
        By_num = xpx.at(By_num)[...].multiply(xp.abs(By_num))

    Bx_den = i/(n+1) * (1 - i/(n+1)) * m*(m+n)/n
    By_den = j/(m+1) * (1 - j/(m+1)) * n*(m+n)/m

    Bx = 1/n * xp.sum(Bx_num/Bx_den, axis=axis)
    By = 1/m * xp.sum(By_num/By_den, axis=axis)

    B = (Bx + By) / 2 if alternative == 'two-sided' else (Bx - By) / 2

    return B

