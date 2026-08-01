
def construct_1d_arraylike_from_scalar(
    value: Scalar, length: int, dtype: DtypeObj | None
) -> ArrayLike:
    """
    create an np.ndarray / pandas type of specified shape and dtype
    filled with values

    Parameters
    ----------
    value : scalar value
    length : int
    dtype : pandas_dtype or np.dtype

    Returns
    -------
    np.ndarray / pandas type of length, filled with value

    """

    if dtype is None:
        try:
            dtype, value = infer_dtype_from_scalar(value)
        except OutOfBoundsDatetime:
            dtype = _dtype_obj

    if isinstance(dtype, ExtensionDtype):
        cls = dtype.construct_array_type()
        seq = [] if length == 0 else [value]
        return cls._from_sequence(seq, dtype=dtype).repeat(length)

    if length and dtype.kind in "iu" and isna(value):
        # coerce if we have nan for an integer dtype
        dtype = np.dtype("float64")
    elif lib.is_np_dtype(dtype, "US"):
        # we need to coerce to object dtype to avoid
        # to allow numpy to take our string as a scalar value
        dtype = np.dtype("object")
        if not isna(value):
            value = ensure_str(value)
    elif dtype.kind in "mM":
        value = _maybe_box_and_unbox_datetimelike(value, dtype)

    subarr = np.empty(length, dtype=dtype)
    if length:
        # GH 47391: numpy > 1.24 will raise filling np.nan into int dtypes
        subarr.fill(value)

    return subarr

