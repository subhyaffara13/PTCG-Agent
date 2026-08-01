
def _histogram(a, numbins=10, defaultlimits=None, weights=None, *,
               density=False, cumulative=False):
    """Create a histogram.

    Separate the range into several bins and return the number of instances
    in each bin.

    Parameters
    ----------
    a : array_like
        Array of scores which will be put into bins.
    numbins : int, optional
        The number of bins to use for the histogram. Default is 10.
    defaultlimits : tuple (lower, upper), optional
        The lower and upper values for the range of the histogram.
        If no value is given, a range slightly larger than the range of the
        values in a is used. Specifically ``(a.min() - s, a.max() + s)``,
        where ``s = (1/2)(a.max() - a.min()) / (numbins - 1)``.
    weights : array_like, optional
        The weights for each value in `a`. Default is None, which gives each
        value a weight of 1.0

    Returns
    -------
    count : ndarray
        Number of points (or sum of weights) in each bin.
    lowerlimit : float
        Lowest value of histogram, the lower limit of the first bin.
    binsize : float
        The size of the bins (all bins have the same size).
    extrapoints : int
        The number of points outside the range of the histogram.

    See Also
    --------
    numpy.histogram

    Notes
    -----
    This histogram is based on numpy's histogram but has a larger range by
    default if default limits is not set.

    """
    xp = array_namespace(a)
    a = xp_ravel(a)
    a, weights = xp_promote(a, weights, force_floating=True, xp=xp)

    if defaultlimits is None:
        if xp_size(a) == 0:
            # handle empty arrays. Undetermined range, so use 0-1.
            defaultlimits = xp.asarray(0., dtype=a.dtype), xp.asarray(1., dtype=a.dtype)
        else:
            # no range given, so use values in `a`
            data_min = xp.min(a)
            data_max = xp.max(a)
            # Have bins extend past min and max values slightly
            s = (data_max - data_min) / (2. * (numbins - 1.))
            defaultlimits = (data_min - s, data_max + s)
    else:
        if not (np.iterable(defaultlimits) and len(defaultlimits)==2
                and defaultlimits[0] < defaultlimits[1]):
            message = ('If specified, `defaultreallimits` must be given as an iterable '
                       'in the order (lower limit, upper limit).')
            raise ValueError(message)
        if not (xp.isdtype(a.dtype, 'real floating')
                and (weights is None or xp.isdtype(weights.dtype, 'real floating'))):
            message = '`a` and (if specified) `weights` must have real dtype.'
            raise ValueError(message)
        if weights is not None and not is_lazy_array(weights) and xp.any(weights < 0):
            message = 'All `weights` must be non-negative.'
            raise ValueError(message)

    bin_edges = xp.linspace(*defaultlimits, numbins+1, dtype=a.dtype)
    if weights is None:
        indices = xp.searchsorted(xp.sort(a), bin_edges, side='left')
        hist = xp.diff(indices)
        n_right_limit = xp.count_nonzero(a == bin_edges[-1])
        hist = xpx.at(hist)[-1].add(xp.astype(n_right_limit, hist.dtype))
    else:
        i = xp.argsort(a)
        weights, a = weights[i], a[i]
        cumulative_weights = xp.cumulative_sum(weights, include_initial=True)
        indices = xp.searchsorted(a, bin_edges, side='left')
        hist = xp.diff(xp.take_along_axis(cumulative_weights, indices, axis=-1))
        hist = xpx.at(hist)[-1].add(xp.sum(xp.where(a == bin_edges[-1], weights, 0.)))

    # fixed width for bins is assumed, as numpy's histogram gives
    # fixed width bins for int values for 'bins'
    binsize = bin_edges[1] - bin_edges[0]
    # calculate number of extra points
    binnedpoints = (xp.sum(hist) if weights is None
                    else xp.count_nonzero((bin_edges[0] <= a) & (a <= bin_edges[-1])))
    extrapoints = a.shape[0] - binnedpoints

    lowerlimit = xp.asarray(defaultlimits[0], dtype=a.dtype)[()]

    hist = xp.asarray(hist, dtype=a.dtype)
    if density:
        hist = hist / (a.shape[0] if weights is None else cumulative_weights[-1])
    if cumulative:
        hist = xp.cumulative_sum(hist, axis=0)

    return HistogramResult(hist, lowerlimit, binsize, extrapoints)

