
def minimum_filter(input, size=None, footprint=None, output=None,
                   mode="reflect", cval=0.0, origin=0, *, axes=None):
    """Calculate a multidimensional minimum filter.

    Parameters
    ----------
    %(input)s
    %(size_foot)s
    %(output)s
    %(mode_multiple)s
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
    minimum_filter : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    A sequence of modes (one per axis) is only supported when the footprint is
    separable. Otherwise, a single mode string must be provided.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.minimum_filter(ascent, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    return _min_or_max_filter(input, size, footprint, None, output, mode,
                              cval, origin, 1, axes)

