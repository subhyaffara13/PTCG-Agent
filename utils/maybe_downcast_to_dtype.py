
def maybe_downcast_to_dtype(result: np.ndarray, dtype: np.dtype) -> np.ndarray: ...


def maybe_downcast_to_dtype(
    result: ExtensionArray, dtype: np.dtype
) -> ExtensionArray: ...


def maybe_downcast_to_dtype(result: ArrayLike, dtype: np.dtype) -> ArrayLike:
    """
    try to cast to the specified dtype (e.g. convert back to bool/int
    or could be an astype of float64->float32
    """
    if isinstance(result, ABCSeries):
        result = result._values
    do_round = False

    if not isinstance(dtype, np.dtype):
        # enforce our signature annotation
        raise TypeError(dtype)  # pragma: no cover

    converted = maybe_downcast_numeric(result, dtype, do_round)
    if converted is not result:
        return converted

    # a datetimelike
    # GH12821, iNaT is cast to float
    if dtype.kind in "mM" and result.dtype.kind in "if":
        result = result.astype(dtype)

    elif dtype.kind == "m" and result.dtype == _dtype_obj:
        # test_where_downcast_to_td64
        result = cast(np.ndarray, result)
        result = array_to_timedelta64(result)

    elif dtype == np.dtype("M8[ns]") and result.dtype == _dtype_obj:
        result = cast(np.ndarray, result)
        return np.asarray(maybe_cast_to_datetime(result, dtype=dtype))

    return result

