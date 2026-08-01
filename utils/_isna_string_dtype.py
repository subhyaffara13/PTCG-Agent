
def _isna_string_dtype(values: np.ndarray) -> npt.NDArray[np.bool_]:
    # Working around NumPy ticket 1542
    dtype = values.dtype

    if dtype.kind in ("S", "U"):
        result = np.zeros(values.shape, dtype=bool)
    elif values.ndim in {1, 2}:
        result = libmissing.isnaobj(values)
    else:
        # 0-D, reached via e.g. mask_missing
        result = libmissing.isnaobj(values.ravel())
        result = result.reshape(values.shape)

    return result

