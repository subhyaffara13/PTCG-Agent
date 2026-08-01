
def _pval_cvm_2samp_asymptotic(t, N, nx, ny, k, *, xp):
    # compute expected value and variance of T (eq. 11 and 14 in [2])
    nx, ny = xp.asarray(nx, dtype=t.dtype), xp.asarray(ny, dtype=t.dtype)
    et = (1 + 1 / N) / 6
    vt = (N + 1) * (4 * k * N - 3 * (nx ** 2 + ny ** 2) - 2 * k)
    vt = vt / (45 * N ** 2 * 4 * k)

    # computed the normalized statistic (eq. 15 in [2])
    tn = 1 / 6 + (t - et) / xp.sqrt(45 * vt)

    # approximate distribution of tn with limiting distribution
    # of the one-sample test statistic
    # if tn < 0.003, the _cdf_cvm_inf(tn) < 1.28*1e-18, return 1.0 directly
    p = xpx.apply_where(tn >= 0.003,
                        (tn,),
                        lambda tn: xp.clip(1. - _cdf_cvm_inf(tn, xp=xp), 0.),
                        fill_value = 1.)
    return p

