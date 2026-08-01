
def _rankdata(x, method, return_sorted=False, return_ties=False, xp=None):
    # Rank data `x` by desired `method`. For methods other than 'ordinal':
    # - `return_sorted=True` ensures that the second output is sorted `x`
    # - `return_ties=True` ensures that the third output is tie data
    # Otherwise, the second/third output will be None.
    xp = array_namespace(x) if xp is None else xp
    dtype = xp_result_type(x, force_floating=True, xp=xp)

    if is_jax(xp):
        import jax.scipy.stats as jax_stats
        ranks = jax_stats.rankdata(x, method=method, axis=-1)
        ranks = xp.astype(ranks, dtype, copy=False)
        y = xp.sort(x, axis=-1) if (return_ties or return_sorted) else None
        t = None
        if return_ties:
            max_ranks = jax_stats.rankdata(y, method='max', axis=-1)
            t = xp.diff(max_ranks, axis=-1, prepend=0)
            t = xp.astype(t, dtype, copy=False)
        return ranks, y, t

    if is_marray(xp):
        data, mask = x.data, x.mask
        uxp = array_namespace(data)
        data = uxp.where(mask, uxp.nan, data)
        ranks, sorted, ties = _rankdata(data, method, return_sorted, return_ties, uxp)
        ranks = xp.asarray(ranks, mask=mask)
        mask_sorted = uxp.isnan(sorted) if (return_sorted or return_ties) else None
        sorted = xp.asarray(sorted, mask=mask_sorted) if return_sorted else None
        ties = xp.asarray(ties, mask=mask_sorted) if return_ties else None
        return ranks, sorted, ties

    shape = x.shape

    # Get sort order
    j = xp.argsort(x, axis=-1, stable=True)
    ordinal_ranks = xp.broadcast_to(xp.arange(1, shape[-1]+1, dtype=dtype), shape)

    # Ordinal ranks is very easy because ties don't matter. We're done.
    if method == 'ordinal':
        ranks = _order_ranks(ordinal_ranks, j, xp=xp)
        return (ranks, None, None)

    # Sort array
    y = xp.take_along_axis(x, j, axis=-1)
    # Logical indices of unique elements
    i = xp.concat([xp.ones(shape[:-1] + (1,), dtype=xp.bool),
                   y[..., :-1] != y[..., 1:]], axis=-1)

    # Integer indices of unique elements
    indices = xp.arange(xp_size(y))[xp.reshape(i, (-1,))]  # i gets raveled
    # Counts of unique elements
    counts = xp.diff(indices, append=xp.asarray([xp_size(y)], dtype=indices.dtype))

    # Compute `'min'`, `'max'`, and `'mid'` ranks of unique elements
    if method == 'min':
        ranks = ordinal_ranks[i]
    elif method == 'max':
        ranks = ordinal_ranks[i] + xp.astype(counts, dtype) - 1
    elif method == 'average':
        # array API doesn't promote integers to floats
        ranks = ordinal_ranks[i] + (xp.astype(counts, dtype) - 1)/2
    elif method == 'dense':
        ranks = xp.cumulative_sum(xp.astype(i, dtype, copy=False), axis=-1)[i]

    if not is_cupy(xp):
        ranks = xp.reshape(xp.repeat(ranks, counts), shape)
    else:
        # workaround for cupy.repeat not accepting arrays for repeats
        # (ref https://github.com/cupy/cupy/issues/3849).
        # The cumulative sum over i will
        # increment every time a new unique rank appears, giving the correct
        # indices to replicate xp.repeats.
        ranks = xp.reshape(
            ranks[xp.cumulative_sum(xp.astype(xp.reshape(i, (-1,)), xp.int64)) - 1],
            shape,
        )
    ranks = _order_ranks(ranks, j, xp=xp)

    t = None
    if return_ties:
        # Tie information is returned in a format that is useful to functions that
        # rely on this (private) function. Example:
        # >>> x = np.asarray([3, 2, 1, 2, 2, 2, 1])
        # >>> _, t = _rankdata(x, 'average', return_ties=True)
        # >>> t  # array([2., 0., 4., 0., 0., 0., 1.])  # two 1s, four 2s, and one 3
        # Unlike ranks, tie counts are *not* reordered to correspond with the order of
        # the input; e.g. the number of appearances of the lowest rank element comes
        # first. This is a useful format because:
        # - The shape of the result is the shape of the input. Different slices can
        #   have different numbers of tied elements but not result in a ragged array.
        # - Functions that use `t` usually don't need to which each element of the
        #   original array is associated with each tie count; they perform a reduction
        #   over the tie counts onnly. The tie counts are naturally computed in a
        #   sorted order, so this does not unnecessarily reorder them.
        # - One exception is `wilcoxon`, which needs the number of zeros. Zeros always
        #   have the lowest rank, so it is easy to find them at the zeroth index.
        t = xp.zeros(shape, dtype=dtype)
        t = xpx.at(t)[i].set(xp.astype(counts, dtype, copy=False))

    return ranks, y, t

