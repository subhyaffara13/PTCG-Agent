
def _robust_slopes(y, *, x, alpha=None, method, pfun):
    other_method = 'joint' if pfun == 'theilslopes' else 'hierarchical'
    if method not in {other_method, 'separate'}:
        raise ValueError(f"method must be either '{other_method}' or 'separate'. "
                         f"'{method}' is invalid.")

    xp = array_namespace(y, x)
    y, x = xp_promote(y, x, force_floating=True, xp=xp)
    x = xp.arange(y.shape[-1], dtype=y.dtype) if x is None else x
    y, x = xp.broadcast_arrays(y, x)
    x, y = _share_masks(x, y, xp=xp)

    if x.shape[-1] < 2 or y.shape[-1] < 2:  # only needed by test_axis_nan_policy
        raise ValueError("`x` and `y` must have length at least 2.")

    # Compute sorted slopes only when deltax > 0
    deltax = x[..., :, xp.newaxis] - x[..., xp.newaxis, :]
    deltay = y[..., :, xp.newaxis] - y[..., xp.newaxis, :]

    if pfun == 'theilslopes':
        i = xp.astype(xp.triu(xp.ones(deltax.shape[-2:]), k=1), xp.bool)
        if is_numpy(xp):
            deltax, deltay = deltax[..., i], deltay[..., i]
        else:
            # With array API, mask must be sole index, so we need to broadcast it.
            # Indexing ravels the array, so we need to reshape the results.
            i = xp.broadcast_to(i, deltax.shape)
            deltax, deltay = deltax[i], deltay[i]
            deltax = xp.reshape(deltax, (*i.shape[:-2], -1))
            deltay = xp.reshape(deltay, (*i.shape[:-2], -1))

    # Use `.data` to avoid indexing with masked indices. If masked elements of deltax=0,
    # they can safely be set to xp.nan, too - they're masked, after all.
    deltax0 = (deltax.data == 0) if is_marray(xp) else (deltax == 0)
    deltax = xpx.at(deltax)[deltax0].set(xp.nan)
    slopes = deltay / deltax

    if is_marray(xp):
        def nanmedian(x, axis):  # use mask to ignore NaNs
            x_nans_masked = xp.asarray(x.data, mask=x.mask | x._xp.isnan(x.data))
            return stats.quantile(x_nans_masked, 0.5, axis=axis)
    else:
        def nanmedian(x, axis):  # use nan_policy to ignore NaNs
            return stats.quantile(x, 0.5, axis=axis, nan_policy='omit')

    def median(x, axis): return stats.quantile(x, 0.5, axis=axis)

    # `theilslopes` is median of all slopes. Indexing with `i` above has already raveled
    # all the slopes, so we only need to take the median along the last axis.
    # `siegelslope` is a median of medians: we take the median of slopes from point i
    # to all other points, then the median of those medians.
    # The slope is NaN wherever the two points are the same, and those don't contribute,
    # hence the first median omits NaNs. NaNs in the input are propagated by the
    # `_axis_nan_policy` decorator.
    medslope = (median(nanmedian(slopes, axis=-1), axis=-1) if pfun == 'siegelslopes'
                else nanmedian(slopes, axis=-1))

    if method in {'joint', 'hierarchical'}:
        medinter = median(y - medslope[..., np.newaxis] * x, axis=-1)
    elif pfun == 'theilslopes':
        medinter = median(y, axis=-1) - medslope * median(x, axis=-1)
    else:
        # Calculate pairwise intercepts given each point (row i) and the slope to each
        # other point (column j). Then calculate the median of (row) medians.
        intercepts = y[..., :, xp.newaxis] - slopes*x[..., :, xp.newaxis]
        medinter = median(nanmedian(intercepts, axis=-1), axis=-1)

    if pfun == 'siegelslopes':
        return SiegelslopesResult(slope=medslope[()], intercept=medinter[()])

    # Now compute confidence intervals
    if alpha > 0.5:
        alpha = 1. - alpha

    z = float(special.ndtri(alpha / 2.))
    # This implements (2.6) from Sen (1968)
    # we don't actually need ranks, so an enhancement could be to have
    # `rankdata` return only the third output. In the meantime, use the
    # least expensive `method`.
    _, _, nxreps = _rankdata(x, method='min', return_ties=True)
    _, _, nyreps = _rankdata(y, method='min', return_ties=True)
    nt = xp.count_nonzero(xp.isfinite(slopes), axis=-1, keepdims=True)  # N in Sen 1968
    nt = xp.asarray(nt, dtype=y.dtype)
    ny = _count_nonmasked(y, keepdims=True, axis=-1)                    # n in Sen 1968
    # Equation 2.6 in Sen (1968):
    sigsq = 1/18. * (
        ny * (ny-1) * (2*ny+5)
        - xp.sum(nxreps * (nxreps-1) * (2*nxreps + 5), axis=-1, keepdims=True)
        - xp.sum(nyreps * (nyreps-1) * (2*nyreps + 5), axis=-1, keepdims=True))
    # Find the confidence interval indices in `slopes`
    sigma = xp.sqrt(xp.maximum(sigsq, xp.zeros_like(sigsq)))
    Ru = xp.minimum(xp.astype(xp.round((nt - z*sigma)/2.), xp.int64),
                    xp.astype(nt, xp.int64)-1)
    Rl = xp.maximum(xp.astype(xp.round((nt + z*sigma)/2.), xp.int64) - 1,
                    xp.asarray(0, dtype=xp.int64))
    R = xp.concat((xpx.atleast_nd(Rl, ndim=1), xpx.atleast_nd(Ru, ndim=1)), axis=-1)
    slopes = xp.sort(slopes, axis=-1)
    delta = xp.take_along_axis(slopes, R, axis=-1)
    i_nan = xp.broadcast_to(sigsq < 0, delta.shape)
    delta = xpx.at(delta)[i_nan].set(xp.nan)

    slope = medslope[()] if medslope.ndim == 0 else medslope
    intercept = medinter[()] if medinter.ndim == 0 else medinter
    low_slope = delta[..., 0]
    high_slope = delta[..., 1]
    low_slope = low_slope[()] if low_slope.ndim == 0 else low_slope
    high_slope = high_slope[()] if high_slope.ndim == 0 else high_slope
    return TheilslopesResult(slope=slope, intercept=intercept,
                             low_slope=low_slope, high_slope=high_slope)

