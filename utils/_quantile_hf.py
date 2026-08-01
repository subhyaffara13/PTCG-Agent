
def _quantile_hf(y, p, n, method, weights, xp):
    ms = dict(inverted_cdf=0, averaged_inverted_cdf=0, closest_observation=-0.5,
              interpolated_inverted_cdf=0, hazen=0.5, weibull=p, linear=1 - p,
              median_unbiased=p/3 + 1/3, normal_unbiased=p/4 + 3/8)
    m = ms[method]

    if weights is None:
        jg = p * n + m
        jp1 = jg // 1
        j = jp1 - 1
    else:
        cumulative_weights = xp.cumulative_sum(weights, axis=-1)
        n_int = xp.asarray(n, dtype=xp.int64)
        n_int = xp.broadcast_to(n_int, cumulative_weights.shape[:-1] + (1,))
        total_weight = xp.take_along_axis(cumulative_weights, n_int-1, axis=-1)
        jg = p * total_weight + m
        jp1 = _xp_searchsorted(cumulative_weights, jg, side='right')
        j = _xp_searchsorted(cumulative_weights, jg-1, side='right')
        j, jp1 = xp.astype(j, y.dtype), xp.astype(jp1, y.dtype)

    g = jg % 1
    if method == 'inverted_cdf':
        g = xp.astype((g > 0), jg.dtype)
    elif method == 'averaged_inverted_cdf':
        g = (1 + xp.astype((g > 0), jg.dtype)) / 2
    elif method == 'closest_observation':
        g = (1 - xp.astype((g == 0) & (j % 2 == 1), jg.dtype))
    if method in {'inverted_cdf', 'averaged_inverted_cdf', 'closest_observation'}:
        g = xp.asarray(g)
        g = xpx.at(g, jg < 0).set(0)

    g = xpx.at(g)[j < 0].set(0)
    j = xp.clip(j, 0., n - 1)
    jp1 = xp.clip(jp1, 0., n - 1)

    return ((1 - g) * xp.take_along_axis(y, xp.astype(j, xp.int64), axis=-1)
            + g * xp.take_along_axis(y, xp.astype(jp1, xp.int64), axis=-1))

