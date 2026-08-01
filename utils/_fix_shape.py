
def _fix_shape(x, shape, axes):
    """Internal auxiliary function for _raw_fft, _raw_fftnd."""
    must_copy = False

    # Build an nd slice with the dimensions to be read from x
    index = [slice(None)]*x.ndim
    for n, ax in zip(shape, axes):
        if x.shape[ax] >= n:
            index[ax] = slice(0, n)
        else:
            index[ax] = slice(0, x.shape[ax])
            must_copy = True

    index = tuple(index)

    if not must_copy:
        return x[index], False

    s = list(x.shape)
    for n, axis in zip(shape, axes):
        s[axis] = n

    z = np.zeros(s, x.dtype)
    z[index] = x[index]
    return z, True

