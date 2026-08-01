
def rank_filter(input, rank, size=None, footprint=None, output=None,
                mode="reflect", cval=0.0, origin=0, *, axes=None):
    """Calculate a multidimensional rank filter.

    Parameters
    ----------
    %(input)s
    rank : int
        The rank parameter may be less than zero, i.e., rank = -1
        indicates the largest element.
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
    rank_filter : ndarray
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
    >>> result = ndimage.rank_filter(ascent, rank=42, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    rank = operator.index(rank)
    return _rank_filter(input, rank, size, footprint, output, mode, cval,
                        origin, 'rank', axes=axes)

