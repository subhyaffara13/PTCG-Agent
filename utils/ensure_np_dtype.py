
def ensure_np_dtype(dtype: DtypeObj) -> np.dtype:
    # TODO: https://github.com/pandas-dev/pandas/issues/22791
    # Give EAs some input on what happens here. Sparse needs this.
    if isinstance(dtype, SparseDtype):
        dtype = dtype.subtype
        dtype = cast(np.dtype, dtype)
    elif isinstance(dtype, ExtensionDtype):
        dtype = np.dtype("object")
    elif dtype == np.dtype(str):
        dtype = np.dtype("object")
    return dtype

