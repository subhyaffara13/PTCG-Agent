
def percentile_filter(input, percentile, size=None, footprint=None,
                      output=None, mode="reflect", cval=0.0, origin=0, *,
                      axes=None):
    """Calculate a multidimensional percentile filter.

    Parameters
    ----------
    %(input)s
    percentile : scalar
        The percentile parameter may be less than zero, i.e.,
        percentile = -20 equals percentile = 80
    %(size_foot)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin_multiple)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `size`, `origin`, and/or `mode`
        must match the length of `axes`. The ith entry in any of these tuples
        corresponds to the ith entry in `axes`.

    Returns
    -------
    percentile_filter : ndarray
        Filtered array. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.percentile_filter(ascent, percentile=20, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    return _rank_filter(input, percentile, size, footprint, output, mode,
                        cval, origin, 'percentile', axes=axes)

