
def medfilt(volume, kernel_size=None):
    """
    Perform a median filter on an N-dimensional array.

    Apply a median filter to the input array using a local window-size
    given by `kernel_size`. The array will automatically be zero-padded.

    Parameters
    ----------
    volume : array_like
        An N-dimensional input array.
    kernel_size : array_like, optional
        A scalar or an N-length list giving the size of the median filter
        window in each dimension.  Elements of `kernel_size` should be odd.
        If `kernel_size` is a scalar, then this scalar is used as the size in
        each dimension. Default size is 3 for each dimension.

    Returns
    -------
    out : ndarray
        An array the same size as input containing the median filtered
        result.

    Warns
    -----
    UserWarning
        If array size is smaller than kernel size along any dimension

    See Also
    --------
    scipy.ndimage.median_filter
    scipy.signal.medfilt2d

    """
    xp = array_namespace(volume)
    volume = xp.asarray(volume)
    if volume.ndim == 0:
        volume = xpx.atleast_nd(volume, ndim=1, xp=xp)

    if not (xp.isdtype(volume.dtype, "integral") or
            volume.dtype in [xp.float32, xp.float64]):
        raise ValueError(f"dtype={volume.dtype} is not supported by medfilt")

    if kernel_size is None:
        kernel_size = [3] * volume.ndim
    kernel_size = xp.asarray(kernel_size)
    if kernel_size.shape == ():
        kernel_size = xp.repeat(kernel_size, volume.ndim)

    for k in range(volume.ndim):
        if (kernel_size[k] % 2) != 1:
            raise ValueError("Each element of kernel_size should be odd.")
    if any(k > s for k, s in zip(kernel_size, volume.shape)):
        warnings.warn('kernel_size exceeds volume extent: the volume will be '
                      'zero-padded.',
                      stacklevel=2)

    size = math.prod(kernel_size)
    result = ndimage.rank_filter(volume, size // 2, size=kernel_size,
                                 mode='constant')

    return result

