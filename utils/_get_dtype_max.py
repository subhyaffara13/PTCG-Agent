
def _get_dtype_max(dtype: np.dtype) -> np.dtype:
    # return a platform independent precision dtype
    dtype_max = dtype
    if dtype.kind in "bi":
        dtype_max = np.dtype(np.int64)
    elif dtype.kind == "u":
        dtype_max = np.dtype(np.uint64)
    elif dtype.kind == "f":
        dtype_max = np.dtype(np.float64)
    return dtype_max

