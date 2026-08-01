
def _log_mean(logx, axis):
    # compute log of mean of x from log(x)
    return (
        special.logsumexp(logx, axis=axis, keepdims=True)
        - math.log(logx.shape[axis])
    )

