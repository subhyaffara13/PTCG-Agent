
def _desc_stats(x1, x2, axis=0, *, xp=None):
    xp = array_namespace(x1, x2) if xp is None else xp

    def _stats(x, axis=0):
        x = xp.asarray(x)
        mu = xp.mean(x, axis=axis)
        std = xp.std(x, axis=axis, correction=1)
        nobs = x.shape[axis]
        return mu, std, nobs

    return _stats(x1, axis) + _stats(x2, axis)

