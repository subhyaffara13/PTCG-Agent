
def _quantile_hd(y, p, n, xp):
    # RE axis handling: We need to perform a reducing operation over rows of `y` for
    # each element in the corresponding row of `p` (a la Cartesian product). Strategy:
    # move rows of `p` to an axis at the front that is orthogonal to all the rest,
    # perform the reducing operating over the last axis, then move the front axis back
    # to the end.
    p = xp.moveaxis(p, -1, 0)[..., xp.newaxis]
    a = p * (n + 1)
    b = (1 - p) * (n + 1)
    i = xp.arange(y.shape[-1] + 1, dtype=y.dtype, device=xp_device(y))
    w = betainc(a, b, i / n)
    w = w[..., 1:] - w[..., :-1]
    w = xpx.at(w, xp.isnan(w)).set(0)
    res = xp.vecdot(w, y, axis=-1)
    return xp.moveaxis(res, 0, -1)

