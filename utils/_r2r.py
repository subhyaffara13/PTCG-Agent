
def _r2r(forward, transform, x, type=2, n=None, axis=-1, norm=None,
         overwrite_x=False, workers=None, orthogonalize=None):
    """Forward or backward 1-D DCT/DST

    Parameters
    ----------
    forward : bool
        Transform direction (determines type and normalisation)
    transform : {pyduccfft.dct, pyduccfft.dst}
        The transform to perform
    """
    tmp = _asfarray(x)
    overwrite_x = overwrite_x or _datacopied(tmp, x)
    norm = _normalization(norm, forward)
    workers = _workers(workers)

    if not forward:
        if type == 2:
            type = 3
        elif type == 3:
            type = 2

    if n is not None:
        tmp, copied = _fix_shape_1d(tmp, n, axis)
        overwrite_x = overwrite_x or copied
    elif tmp.shape[axis] < 1:
        raise ValueError(f"invalid number of data points ({tmp.shape[axis]}) specified")

    out = (tmp if overwrite_x else None)

    # For complex input, transform real and imaginary components separably
    if np.iscomplexobj(x):
        out = np.empty_like(tmp) if out is None else out
        transform(tmp.real, type, (axis,), norm, out.real, workers)
        transform(tmp.imag, type, (axis,), norm, out.imag, workers)
        return out

    return transform(tmp, type, (axis,), norm, out, workers, orthogonalize)

