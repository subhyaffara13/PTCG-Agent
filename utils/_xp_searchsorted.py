import math


def _xp_searchsorted(x, y, *, side='left', xp=None):
    # Vectorized xp.searchsorted. Search is performed along last axis. The shape of the
    # output is that of `y`, broadcasting the batch dimensions with those of `x` if
    # necessary.
    xp = array_namespace(x, y) if xp is None else xp
    xp_default_int = xp.asarray(1).dtype
    y_0d = xp.asarray(y).ndim == 0
    x, y = _broadcast_arrays((x, y), axis=-1, xp=xp)
    x_1d = x.ndim <= 1

    if x_1d or is_torch(xp):
        y = xp.reshape(y, ()) if (y_0d and x_1d) else y
        out = xp.searchsorted(x, y, side=side)
        out = xp.astype(out, xp_default_int, copy=False)
        return out

    a = xp.full(y.shape, 0, device=xp_device(x))

    if x.shape[-1] == 0:
        return a

    n = xp.count_nonzero(~xp.isnan(x), axis=-1, keepdims=True)
    b = xp.broadcast_to(n, y.shape)

    compare = xp.less_equal if side == 'left' else xp.less

    # while xp.any(b - a > 1):
    # refactored to for loop with ~log2(n) iterations for JAX JIT
    for i in range(int(math.log2(x.shape[-1])) + 1):
        c = (a + b) // 2
        x0 = xp.take_along_axis(x, c, axis=-1)
        j = compare(y, x0)
        b = xp.where(j, c, b)
        a = xp.where(j, a, c)

    out = xp.where(compare(y, xp.min(x, axis=-1, keepdims=True)), 0, b)
    out = xp.where(xp.isnan(y), x.shape[-1], out) if side == 'right' else out
    out = xp.astype(out, xp_default_int, copy=False)
    return out

