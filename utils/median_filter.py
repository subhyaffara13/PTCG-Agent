
def median_filter(input, size=None, footprint=None, output=None,
                  mode="reflect", cval=0.0, origin=0, *, axes=None):
    """
    Calculate a multidimensional median filter.

    Parameters
    ----------
    %(input)s
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
    median_filter : ndarray
        Filtered array. Has the same shape as `input`.

    See Also
    --------
    scipy.signal.medfilt2d

    Notes
    -----
    For 2-dimensional images with ``uint8``, ``float32`` or ``float64`` dtypes
    the specialised function `scipy.signal.medfilt2d` may be faster. It is
    however limited to constant mode with ``cval=0``.

    The filter always returns the argument that would appear at index ``n // 2`` in
    a sorted array, where ``n`` is the number of elements in the footprint of the
    filter. Note that this differs from the conventional definition of the median
    when ``n`` is even. Also, this function does not support the ``float16`` dtype,
    behavior in the presence of NaNs is undefined, and memory consumption scales with
    ``n**4``. For ``float16`` support, greater control over the definition of the
    filter, and to limit memory usage, consider using `vectorized_filter` with
    NumPy functions `np.median` or `np.nanmedian`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.median_filter(ascent, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    return _rank_filter(input, 0, size, footprint, output, mode, cval,
                        origin, 'median', axes=axes)

