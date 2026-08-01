
def _quantile_winsor(y, p, n, method, xp):
    ops = dict(round_outward=(xp.floor, xp.ceil),
               round_inward=(xp.ceil, xp.floor),
               round_nearest=(xp.round, xp.round))
    op_left, op_right = ops[method]
    j = xp.where(p < 0.5, op_left(p*n), op_right(n*p - 1))
    return xp.take_along_axis(y, xp.astype(j, xp.int64), axis=-1)

