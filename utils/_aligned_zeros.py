import functools

def _aligned_zeros(shape, dtype=float, order="C", align=None):
    """
    Allocate a new ndarray with aligned memory.

    The ndarray is guaranteed *not* aligned to twice the requested alignment.
    Eg, if align=4, guarantees it is not aligned to 8. If align=None uses
    dtype.alignment."""
    dtype = np.dtype(dtype)
    if dtype == np.dtype(object):
        # Can't do this, fall back to standard allocation (which
        # should always be sufficiently aligned)
        if align is not None:
            raise ValueError("object array alignment not supported")
        return np.zeros(shape, dtype=dtype, order=order)
    if align is None:
        align = dtype.alignment
    if not hasattr(shape, '__len__'):
        shape = (shape,)
    size = functools.reduce(operator.mul, shape) * dtype.itemsize
    buf = np.empty(size + 2 * align + 1, np.uint8)

    ptr = buf.__array_interface__['data'][0]
    offset = ptr % align
    if offset != 0:
        offset = align - offset
    if (ptr % (2 * align)) == 0:
        offset += align

    # Note: slices producing 0-size arrays do not necessarily change
    # data pointer --- so we use and allocate size+1
    buf = buf[offset:offset + size + 1][:-1]
    buf.fill(0)
    data = np.ndarray(shape, dtype, buf, order=order)
    return data

