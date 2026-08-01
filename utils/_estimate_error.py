
def _estimate_error(work, xp):
    # Estimate the error according to [1] Section 5

    if work.n == 0 or work.nit == 0:
        # The paper says to use "one" as the error before it can be calculated.
        # NaN seems to be more appropriate.
        nan = xp.full_like(work.Sn, xp.nan)
        return nan, nan

    indices = work.pair_cache.indices

    n_active = work.Sn.shape[0]  # number of active elements
    axis_kwargs = dict(axis=-1, keepdims=True)

    # With a jump start (starting at level higher than 0), we haven't
    # explicitly calculated the integral estimate at lower levels. But we have
    # all the function value-weight products, so we can compute the
    # lower-level estimates.
    if work.Sk.shape[-1] == 0:
        h = 2 * work.h  # step size at this level
        n_x = indices[work.n]  # number of abscissa up to this level
        # The right and left fjwj terms from all levels are concatenated along
        # the last axis. Get out only the terms up to this level.
        fjwj_rl = xp.reshape(work.fjwj, (n_active, 2, -1))
        fjwj = xp.reshape(fjwj_rl[:, :, :n_x], (n_active, 2*n_x))
        # Compute the Euler-Maclaurin sum at this level
        Snm1 = (special.logsumexp(fjwj, **axis_kwargs) + xp.log(h) if work.log
                else xp.sum(fjwj, **axis_kwargs) * h)
        work.Sk = xp.concat((Snm1, work.Sk), axis=-1)

    if work.n == 1:
        nan = xp.full_like(work.Sn, xp.nan)
        return nan, nan

    # The paper says not to calculate the error for n<=2, but it's not clear
    # about whether it starts at level 0 or level 1. We start at level 0, so
    # why not compute the error beginning in level 2?
    if work.Sk.shape[-1] < 2:
        h = 4 * work.h  # step size at this level
        n_x = indices[work.n-1]  # number of abscissa up to this level
        # The right and left fjwj terms from all levels are concatenated along
        # the last axis. Get out only the terms up to this level.
        fjwj_rl = xp.reshape(work.fjwj, (work.Sn.shape[0], 2, -1))
        fjwj = xp.reshape(fjwj_rl[..., :n_x], (n_active, 2*n_x))
        # Compute the Euler-Maclaurin sum at this level
        Snm2 = (special.logsumexp(fjwj, **axis_kwargs) + xp.log(h) if work.log
                else xp.sum(fjwj, **axis_kwargs) * h)
        work.Sk = xp.concat((Snm2, work.Sk), axis=-1)

    Snm2 = work.Sk[..., -2]
    Snm1 = work.Sk[..., -1]

    e1 = xp.asarray(work.eps)[()]

    if work.log:
        log_e1 = xp.log(e1)
        # Currently, only real integrals are supported in log-scale. All
        # complex values have imaginary part in increments of pi*j, which just
        # carries sign information of the original integral, so use of
        # `xp.real` here is equivalent to absolute value in real scale.
        d1 = xp.real(special.logsumexp(xp.stack([work.Sn, Snm1 + work.pi*1j]), axis=0))
        d2 = xp.real(special.logsumexp(xp.stack([work.Sn, Snm2 + work.pi*1j]), axis=0))
        d3 = log_e1 + xp.max(xp.real(work.fjwj), axis=-1)
        d4 = work.d4
        d5 = log_e1 + xp.real(work.Sn)
        temp = xp.where(d1 > -xp.inf, d1 ** 2 / d2, -xp.inf)
        ds = xp.stack([temp, 2 * d1, d3, d4])
        aerr = xp.clip(xp.max(ds, axis=0), d5, d1)
        rerr = aerr - xp.real(work.Sn)
    else:
        # Note: explicit computation of log10 of each of these is unnecessary.
        d1 = xp.abs(work.Sn - Snm1)
        d2 = xp.abs(work.Sn - Snm2)
        d3 = e1 * xp.max(xp.abs(work.fjwj), axis=-1)
        d4 = work.d4
        d5 = e1 * xp.abs(work.Sn)
        temp = xp.where(d1 > 0, d1**(xp.log(d1)/xp.log(d2)), 0)
        ds = xp.stack([temp, d1**2, d3, d4])
        aerr = xp.clip(xp.max(ds, axis=0), d5, d1)
        rerr = aerr/xp.abs(work.Sn)

    return rerr, aerr

