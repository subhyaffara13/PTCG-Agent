
def _br(x, *, r=0, xp):
    n = x.shape[-1]
    x = xp.expand_dims(x, axis=-2)
    x = xp.broadcast_to(x, x.shape[:-2] + (r.shape[0], n))
    x = xp.triu(x)
    j = xp.arange(n, dtype=x.dtype)
    n = xp.asarray(n, dtype=x.dtype)[()]
    binom_j_r = xpx.lazy_apply(special.binom, j, r[:, xp.newaxis])
    binom_nm1_r = xpx.lazy_apply(special.binom, n-1, r)
    return xp.vecdot(binom_j_r, x, axis=-1) / binom_nm1_r / n

