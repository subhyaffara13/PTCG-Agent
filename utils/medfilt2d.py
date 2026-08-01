
def medfilt2d(input, kernel_size=3):
    """
    Median filter a 2-dimensional array.

    Apply a median filter to the `input` array using a local window-size
    given by `kernel_size` (must be odd). The array is zero-padded
    automatically.

    Parameters
    ----------
    input : array_like
        A 2-dimensional input array.
    kernel_size : array_like, optional
        A scalar or a list of length 2, giving the size of the
        median filter window in each dimension.  Elements of
        `kernel_size` should be odd.  If `kernel_size` is a scalar,
        then this scalar is used as the size in each dimension.
        Default is a kernel of size (3, 3).

    Returns
    -------
    out : ndarray
        An array the same size as input containing the median filtered
        result.

    See Also
    --------
    scipy.ndimage.median_filter

    Notes
    -----
    This is faster than `medfilt` when the input dtype is ``uint8``,
    ``float32``, or ``float64``; for other types, this falls back to
    `medfilt`. In some situations, `scipy.ndimage.median_filter` may be
    faster than this function.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import signal
    >>> x = np.arange(25).reshape(5, 5)
    >>> x
    array([[ 0,  1,  2,  3,  4],
           [ 5,  6,  7,  8,  9],
           [10, 11, 12, 13, 14],
           [15, 16, 17, 18, 19],
           [20, 21, 22, 23, 24]])

    # Replaces i,j with the median out of 5*5 window

    >>> signal.medfilt2d(x, kernel_size=5)
    array([[ 0,  0,  2,  0,  0],
           [ 0,  3,  7,  4,  0],
           [ 2,  8, 12,  9,  4],
           [ 0,  8, 12,  9,  0],
           [ 0,  0, 12,  0,  0]])

    # Replaces i,j with the median out of default 3*3 window

    >>> signal.medfilt2d(x)
    array([[ 0,  1,  2,  3,  0],
           [ 1,  6,  7,  8,  4],
           [ 6, 11, 12, 13,  9],
           [11, 16, 17, 18, 14],
           [ 0, 16, 17, 18,  0]])

    # Replaces i,j with the median out of default 5*3 window

    >>> signal.medfilt2d(x, kernel_size=[5,3])
    array([[ 0,  1,  2,  3,  0],
           [ 0,  6,  7,  8,  3],
           [ 5, 11, 12, 13,  8],
           [ 5, 11, 12, 13,  8],
           [ 0, 11, 12, 13,  0]])

    # Replaces i,j with the median out of default 3*5 window

    >>> signal.medfilt2d(x, kernel_size=[3,5])
    array([[ 0,  0,  2,  1,  0],
           [ 1,  5,  7,  6,  3],
           [ 6, 10, 12, 11,  8],
           [11, 15, 17, 16, 13],
           [ 0, 15, 17, 16,  0]])

    # As seen in the examples,
    # kernel numbers must be odd and not exceed original array dim

    """
    xp = array_namespace(input)

    image = np.asarray(input)

    # checking dtype.type, rather than just dtype, is necessary for
    # excluding np.longdouble with MS Visual C.
    if image.dtype.type not in (np.ubyte, np.float32, np.float64):
        return xp.asarray(medfilt(image, kernel_size))

    if kernel_size is None:
        kernel_size = [3] * 2
    kernel_size = np.asarray(kernel_size)
    if kernel_size.shape == ():
        kernel_size = np.repeat(kernel_size.item(), 2)

    for size in kernel_size:
        if (size % 2) != 1:
            raise ValueError("Each element of kernel_size should be odd.")

    result_np = _sigtools._medfilt2d(image, kernel_size)
    return xp.asarray(result_np)

