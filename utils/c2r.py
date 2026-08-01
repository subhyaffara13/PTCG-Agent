
def c2r(forward, x, n=None, axis=-1, norm=None, overwrite_x=False,
        workers=None, *, plan=None):
    """
    Return inverse discrete Fourier transform of real sequence x.
    """
    if plan is not None:
        raise NotImplementedError('Passing a precomputed plan is not yet '
                                  'supported by scipy.fft functions')
    tmp = _asfarray(x)
    norm = _normalization(norm, forward)
    workers = _workers(workers)

    # TODO: Optimize for hermitian and real?
    if np.isrealobj(tmp):
        tmp = tmp + 0.j

    # Last axis utilizes hermitian symmetry
    if n is None:
        n = (tmp.shape[axis] - 1) * 2
        if n < 1:
            raise ValueError(f"Invalid number of data points ({n}) specified")
    else:
        tmp, _ = _fix_shape_1d(tmp, (n//2) + 1, axis)

    # Note: overwrite_x is not utilized
    return pfft.c2r(tmp, (axis,), n, forward, norm, None, workers)

