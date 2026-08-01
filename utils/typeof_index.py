
def typeof_index(val, c) -> IndexType:
    """
    This will assume that only strings are in object dtype
    index.
    (you should check this before this gets lowered down to numba)
    """
    # arrty = typeof_impl(val._data, c)
    arrty = typeof_impl(val._numba_data, c)
    assert arrty.ndim == 1
    return IndexType(arrty.dtype, arrty.layout, type(val))

