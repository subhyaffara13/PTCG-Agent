
def in1d(
    x1: Array,
    x2: Array,
    /,
    *,
    assume_unique: bool = False,
    invert: bool = False,
    xp: ModuleType | None = None,
) -> Array:  # numpydoc ignore=PR01,RT01
    """
    Check whether each element of an array is also present in a second array.

    Returns a boolean array the same length as `x1` that is True
    where an element of `x1` is in `x2` and False otherwise.

    This function has been adapted using the original implementation
    present in numpy:
    https://github.com/numpy/numpy/blob/v1.26.0/numpy/lib/arraysetops.py#L524-L758
    """
    if xp is None:
        xp = array_namespace(x1, x2)

    x1_shape = eager_shape(x1)
    x2_shape = eager_shape(x2)

    # This code is run to make the code significantly faster
    if x2_shape[0] < 10 * x1_shape[0] ** 0.145 and isinstance(x2, Iterable):
        if invert:
            mask = xp.ones(x1_shape[0], dtype=xp.bool, device=_compat.device(x1))
            for a in x2:
                mask &= x1 != a
        else:
            mask = xp.zeros(x1_shape[0], dtype=xp.bool, device=_compat.device(x1))
            for a in x2:
                mask |= x1 == a
        return mask

    rev_idx = xp.empty(0)  # placeholder
    if not assume_unique:
        x1, rev_idx = xp.unique_inverse(x1)
        x2 = xp.unique_values(x2)

    ar = xp.concat((x1, x2))
    device_ = _compat.device(ar)
    # We need this to be a stable sort.
    order = xp.argsort(ar, stable=True)
    reverse_order = xp.argsort(order, stable=True)
    sar = xp.take(ar, order, axis=0)
    ar_size = _compat.size(sar)
    assert ar_size is not None, "xp.unique*() on lazy backends raises"
    if ar_size >= 1:
        bool_ar = sar[1:] != sar[:-1] if invert else sar[1:] == sar[:-1]
    else:
        bool_ar = xp.asarray([False]) if invert else xp.asarray([True])
    flag = xp.concat((bool_ar, xp.asarray([invert], device=device_)))
    ret = xp.take(flag, reverse_order, axis=0)

    if assume_unique:
        return ret[: x1.shape[0]]
    return xp.take(ret, rev_idx, axis=0)


def in1d(ar1, ar2, assume_unique=False, invert=False):
    """
    Test whether each element of an array is also present in a second
    array.

    The output is always a masked array.

    We recommend using :func:`isin` instead of `in1d` for new code.

    See Also
    --------
    isin       : Version of this function that preserves the shape of ar1.

    Examples
    --------
    >>> import numpy as np
    >>> ar1 = np.ma.array([0, 1, 2, 5, 0])
    >>> ar2 = [0, 2]
    >>> np.ma.in1d(ar1, ar2)
    masked_array(data=[ True, False,  True, False,  True],
                 mask=False,
           fill_value=True)

    """
    if not assume_unique:
        ar1, rev_idx = unique(ar1, return_inverse=True)
        ar2 = unique(ar2)

    ar = ma.concatenate((ar1, ar2))
    # We need this to be a stable sort, so always use 'mergesort'
    # here. The values from the first array should always come before
    # the values from the second array.
    order = ar.argsort(kind='mergesort')
    sar = ar[order]
    if invert:
        bool_ar = (sar[1:] != sar[:-1])
    else:
        bool_ar = (sar[1:] == sar[:-1])
    flag = ma.concatenate((bool_ar, [invert]))
    indx = order.argsort(kind='mergesort')[:len(ar1)]

    if assume_unique:
        return flag[indx]
    else:
        return flag[indx][rev_idx]

