
def _log_var(logx, xp, axis):
    # compute log of variance of x from log(x)
    logmean = xp.broadcast_to(_log_mean(logx, axis=axis), logx.shape)
    ones = xp.ones_like(logx)
    logxmu, _ = special.logsumexp(xp.stack((logx, logmean), axis=0), axis=0,
                                  b=xp.stack((ones, -ones), axis=0), return_sign=True)
    return special.logsumexp(2 * logxmu, axis=axis) - math.log(logx.shape[axis])

