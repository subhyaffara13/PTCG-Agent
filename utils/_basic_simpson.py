
def _basic_simpson(y, start, stop, x, dx, axis, *, xp):
    nd = y.ndim
    if start is None:
        start = 0
    step = 2
    slice_all = (slice(None),)*nd
    slice0 = tupleset(slice_all, axis, slice(start, stop, step))
    slice1 = tupleset(slice_all, axis, slice(start+1, stop+1, step))
    slice2 = tupleset(slice_all, axis, slice(start+2, stop+2, step))

    if x is None:  # Even-spaced Simpson's rule.
        result = dx / 3.0 * xp.sum(y[slice0] + 4.0*y[slice1] + y[slice2], axis=axis)
    else:
        # Account for possibly different spacings.
        #    Simpson's rule changes a bit.
        h = xp.diff(x, axis=axis)
        sl0 = tupleset(slice_all, axis, slice(start, stop, step))
        sl1 = tupleset(slice_all, axis, slice(start+1, stop+1, step))
        h0 = h[sl0] if xp_size(h) else h
        h1 = h[sl1] if xp_size(h) else h
        hsum = h0 + h1
        hprod = h0 * h1
        h0divh1 = xpx.apply_where(h1 != 0, (h0, h1), xp.divide, fill_value=0.)
        tmp = hsum/6.0 * (y[slice0] *
            (2.0 - xpx.apply_where(h0divh1 != 0, (xp.ones_like(h0divh1), h0divh1,),
                                   xp.divide, fill_value=0.))
            + y[slice1] * (hsum * xpx.apply_where(hprod != 0, (hsum, hprod,),
                                                  xp.divide, fill_value=0.))
            + (y[slice2] if xp_size(y) > 1 else y[0:0, ...]) * (2.0 - h0divh1))
        result = xp.sum(tmp, axis=axis)
    return result

