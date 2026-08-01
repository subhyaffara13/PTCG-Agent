
def minimum_filter1d(input, size, axis=-1, output=None,
                     mode="reflect", cval=0.0, origin=0):
    """Calculate a 1-D minimum filter along the given axis.

    The lines of the array along the given axis are filtered with a
    minimum filter of given size.

    Parameters
    ----------
    %(input)s
    size : int
        length along which to calculate 1D minimum
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s

    Returns
    -------
    result : ndarray.
        Filtered image. Has the same shape as `input`.

    Notes
    -----
    This function implements the MINLIST algorithm [1]_, as described by
    Richard Harter [2]_, and has a guaranteed O(n) performance, `n` being
    the `input` length, regardless of filter size.

    References
    ----------
    .. [1] http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.42.2777.
    .. [2] http://www.richardhartersworld.com/cri/2001/slidingmin.html


    Examples
    --------
    >>> from scipy.ndimage import minimum_filter1d
    >>> minimum_filter1d([2, 8, 0, 4, 1, 9, 9, 0], size=3)
    array([2, 0, 0, 0, 1, 1, 0, 0])
    """
    input = np.asarray(input)
    if np.iscomplexobj(input):
        raise TypeError('Complex type not supported')
    axis = normalize_axis_index(axis, input.ndim)
    if size < 1:
        raise RuntimeError('incorrect filter size')
    output = _ni_support._get_output(output, input)
    if (size // 2 + origin < 0) or (size // 2 + origin >= size):
        raise ValueError('invalid origin')
    mode = _ni_support._extend_mode_to_code(mode)
    _nd_image.min_or_max_filter1d(input, size, axis, output, mode, cval,
                                  origin, 1)
    return output

