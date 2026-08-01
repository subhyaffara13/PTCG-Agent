
def _bin_edges(sample, bins=None, range=None):
    """ Create edge arrays
    """
    Dlen, Ndim = sample.shape

    nbin = np.empty(Ndim, int)    # Number of bins in each dimension
    edges = Ndim * [None]         # Bin edges for each dim (will be 2D array)
    dedges = Ndim * [None]        # Spacing between edges (will be 2D array)

    # Preserve sample floating point precision in bin edges
    edges_dtype = (sample.dtype if np.issubdtype(sample.dtype, np.floating)
                   else float)

    # Select range for each dimension
    # Used only if number of bins is given.
    if range is None:
        sample = sample.astype(float, copy=True)
        sample[np.isinf(sample)] = np.nan
        smin = np.atleast_1d(np.nanmin(sample, axis=0))
        smax = np.atleast_1d(np.nanmax(sample, axis=0))
    else:
        if len(range) != Ndim:
            raise ValueError(
                f"range given for {len(range)} dimensions; {Ndim} required")
        smin = np.empty(Ndim)
        smax = np.empty(Ndim)
        for i in builtins.range(Ndim):
            if range[i][1] < range[i][0]:
                raise ValueError(
                    f"In {f'dimension {i + 1} of ' if Ndim > 1 else ''}range,"
                    " start must be <= stop")
            smin[i], smax[i] = range[i]

    # Make sure the bins have a finite width.
    for i in builtins.range(len(smin)):
        if smin[i] == smax[i]:
            smin[i] = smin[i] - .5
            smax[i] = smax[i] + .5

    # Create edge arrays
    for i in builtins.range(Ndim):
        if np.isscalar(bins[i]):
            nbin[i] = bins[i] + 2  # +2 for outlier bins
            edges[i] = np.linspace(smin[i], smax[i], nbin[i] - 1,
                                   dtype=edges_dtype)
        else:
            edges[i] = np.asarray(bins[i], edges_dtype)
            nbin[i] = len(edges[i]) + 1  # +1 for outlier bins
        dedges[i] = np.diff(edges[i])

    nbin = np.asarray(nbin)

    return nbin, edges, dedges

