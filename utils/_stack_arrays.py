
def _stack_arrays(tuples, dtype: np.dtype):
    placement, arrays = zip(*tuples, strict=True)

    first = arrays[0]
    shape = (len(arrays), *first.shape)

    stacked = np.empty(shape, dtype=dtype)
    for i, arr in enumerate(arrays):
        stacked[i] = arr

    return stacked, placement

