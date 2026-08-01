
def convolve1d(input, weights, axis=-1, output=None, mode="reflect",
               cval=0.0, origin=0):
    """Calculate a 1-D convolution along the given axis.

    The lines of the array along the given axis are convolved with the
    given weights.

    Parameters
    ----------
    %(input)s
    weights : ndarray
        1-D sequence of numbers.
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s

    Returns
    -------
    convolve1d : ndarray
        Convolved array with same shape as input

    Examples
    --------
    >>> from scipy.ndimage import convolve1d
    >>> convolve1d([2, 8, 0, 4, 1, 9, 9, 0], weights=[1, 3])
    array([14, 24,  4, 13, 12, 36, 27,  0])
    """
    weights = np.asarray(weights)
    weights = weights[::-1]
    origin = -origin
    if not weights.shape[0] & 1:
        origin -= 1
    if weights.dtype.kind == 'c':
        # pre-conjugate here to counteract the conjugation in correlate1d
        weights = weights.conj()
    return correlate1d(input, weights, axis, output, mode, cval, origin)

