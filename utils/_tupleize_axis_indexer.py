
def _tupleize_axis_indexer(ndim: int, axis: AxisInt, key) -> tuple:
    """
    If we have an axis, adapt the given key to be axis-independent.
    """
    new_key = [slice(None)] * ndim
    new_key[axis] = key
    return tuple(new_key)

