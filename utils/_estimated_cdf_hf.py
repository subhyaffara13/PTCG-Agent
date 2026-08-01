
def _estimated_cdf_hf(x, y, n, method, xp):
    n_int = xp.astype(n, xp.int64)
    j_max = n_int - 1
    j_min = xp.minimum(j_max, xp.asarray(1, dtype=j_max.dtype))
    jp1 = _xp_searchsorted(x, y, side='right')

    if method in _estimated_cdf_discontinuous_methods:
        dp = _estimated_cdf_discontinuous_methods[method]
        p = (xp.astype(jp1, x.dtype)+dp)/n

    else:
        jp1 = xp.clip(jp1, j_min, j_max)
        j = xp.clip(jp1-1, 0)
        xj = xp.take_along_axis(x, j, axis=-1)
        xjp1 = xp.take_along_axis(x, jp1, axis=-1)
        with np.errstate(divide='ignore', invalid='ignore'):  # refactor to apply_where?
            delta = xp.where((xjp1 > xj) & xp.isfinite(xj), (y - xj) / (xjp1 - xj), 1.)

        a, b = _estimated_cdf_continuous_methods[method]
        p = (xp.astype(jp1, x.dtype) + delta - a) / (n + 1 - a - b)

    xmin = x[..., :1]
    xmax = (x[..., -1:] if n.shape == () else xp.take_along_axis(x, j_max))
    p = xpx.at(p)[y < xmin].set(0.)
    p = xpx.at(p)[y > xmax].set(1.)

    return xp.clip(p, 0., 1.)

