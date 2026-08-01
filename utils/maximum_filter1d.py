
def maximum_filter1d(input, size, axis=-1, output=None,
                     mode="reflect", cval=0.0, origin=0):
    """Calculate a 1-D maximum filter along the given axis.

    The lines of the array along the given axis are filtered with a
    maximum filter of given size.

    Parameters
    ----------
    %(input)s
    size : int
        Length along which to calculate the 1-D maximum.
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s

    Returns
    -------
    maximum1d : ndarray, None
        Maximum-filtered array with same shape as input.
        None if `output` is not None

    Notes
    -----
    This function implements the MAXLIST algorithm [1]_, as described by
    Richard Harter [2]_, and has a guaranteed O(n) performance, `n` being
    the `input` length, regardless of filter size.

    References
    ----------
    .. [1] http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.42.2777.
    .. [2] http://www.richardhartersworld.com/cri/2001/slidingmin.html

    Examples
    --------
    >>> from scipy.ndimage import maximum_filter1d
    >>> maximum_filter1d([2, 8, 0, 4, 1, 9, 9, 0], size=3)
    array([8, 8, 8, 4, 9, 9, 9, 9])
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
                                  origin, 0)
    return output

