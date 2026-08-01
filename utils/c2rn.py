
def c2rn(forward, x, s=None, axes=None, norm=None, overwrite_x=False,
         workers=None, *, plan=None):
    """Multidimensional inverse discrete fourier transform with real output"""
    if plan is not None:
        raise NotImplementedError('Passing a precomputed plan is not yet '
                                  'supported by scipy.fft functions')
    tmp = _asfarray(x)

    # TODO: Optimize for hermitian and real?
    if np.isrealobj(tmp):
        tmp = tmp + 0.j

    noshape = s is None
    shape, axes = _init_nd_shape_and_axes(tmp, s, axes)

    if len(axes) == 0:
        raise ValueError("at least 1 axis must be transformed")

    shape = list(shape)
    if noshape:
        shape[-1] = (x.shape[axes[-1]] - 1) * 2

    norm = _normalization(norm, forward)
    workers = _workers(workers)

    # Last axis utilizes hermitian symmetry
    lastsize = shape[-1]
    shape[-1] = (shape[-1] // 2) + 1

    tmp, _ = tuple(_fix_shape(tmp, shape, axes))

    # Note: overwrite_x is not utilized
    return pfft.c2r(tmp, axes, lastsize, forward, norm, None, workers)

