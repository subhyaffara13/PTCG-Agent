
def uniform_filter1d(input, size, axis=-1, output=None,
                     mode="reflect", cval=0.0, origin=0):
    """Calculate a 1-D uniform filter along the given axis.

    The lines of the array along the given axis are filtered with a
    uniform filter of given size.

    Parameters
    ----------
    %(input)s
    size : int
        length of uniform filter
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s

    Returns
    -------
    result : ndarray
        Filtered array. Has same shape as `input`.

    Examples
    --------
    >>> from scipy.ndimage import uniform_filter1d
    >>> uniform_filter1d([2, 8, 0, 4, 1, 9, 9, 0], size=3)
    array([4, 3, 4, 1, 4, 6, 6, 3])
    """
    input = np.asarray(input)
    axis = normalize_axis_index(axis, input.ndim)
    if size < 1:
        raise RuntimeError('incorrect filter size')
    complex_output = input.dtype.kind == 'c'
    output = _ni_support._get_output(output, input,
                                     complex_output=complex_output)
    if (size // 2 + origin < 0) or (size // 2 + origin >= size):
        raise ValueError('invalid origin')
    mode = _ni_support._extend_mode_to_code(mode)
    if not complex_output:
        _nd_image.uniform_filter1d(input, size, axis, output, mode, cval,
                                   origin)
    else:
        _nd_image.uniform_filter1d(input.real, size, axis, output.real, mode,
                                   np.real(cval), origin)
        _nd_image.uniform_filter1d(input.imag, size, axis, output.imag, mode,
                                   np.imag(cval), origin)
    return output

