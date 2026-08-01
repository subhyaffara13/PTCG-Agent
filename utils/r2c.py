
def r2c(forward, x, n=None, axis=-1, norm=None, overwrite_x=False,
        workers=None, *, plan=None):
    """
    Discrete Fourier transform of a real sequence.
    """
    if plan is not None:
        raise NotImplementedError('Passing a precomputed plan is not yet '
                                  'supported by scipy.fft functions')
    tmp = _asfarray(x)
    norm = _normalization(norm, forward)
    workers = _workers(workers)

    if not np.isrealobj(tmp):
        raise TypeError("x must be a real sequence")

    if n is not None:
        tmp, _ = _fix_shape_1d(tmp, n, axis)
    elif tmp.shape[axis] < 1:
        raise ValueError(f"invalid number of data points ({tmp.shape[axis]}) specified")

    # Note: overwrite_x is not utilised
    return pfft.r2c(tmp, (axis,), forward, norm, None, workers)

