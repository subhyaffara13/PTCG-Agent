
def _bin_numbers(sample, nbin, edges, dedges):
    """Compute the bin number each sample falls into, in each dimension
    """
    Dlen, Ndim = sample.shape

    sampBin = [
        np.digitize(sample[:, i], edges[i])
        for i in range(Ndim)
    ]

    # Using `digitize`, values that fall on an edge are put in the right bin.
    # For the rightmost bin, we want values equal to the right
    # edge to be counted in the last bin, and not as an outlier.
    for i in range(Ndim):
        # Find the rounding precision
        dedges_min = dedges[i].min()
        if dedges_min == 0:
            raise ValueError('The smallest edge difference is numerically 0.')
        decimal = int(-np.log10(dedges_min)) + 6
        # Find which points are on the rightmost edge.
        on_edge = np.where((sample[:, i] >= edges[i][-1]) &
                           (np.around(sample[:, i], decimal) ==
                            np.around(edges[i][-1], decimal)))[0]
        # Shift these points one bin to the left.
        sampBin[i][on_edge] -= 1

    # Compute the sample indices in the flattened statistic matrix.
    binnumbers = np.ravel_multi_index(sampBin, nbin)

    return binnumbers

