
def ensure_dtype_can_hold_na(dtype: np.dtype) -> np.dtype: ...


def ensure_dtype_can_hold_na(dtype: ExtensionDtype) -> ExtensionDtype: ...


def ensure_dtype_can_hold_na(dtype: DtypeObj) -> DtypeObj:
    """
    If we have a dtype that cannot hold NA values, find the best match that can.
    """
    if isinstance(dtype, ExtensionDtype):
        if dtype._can_hold_na:
            return dtype
        elif isinstance(dtype, IntervalDtype):
            # TODO(GH#45349): don't special-case IntervalDtype, allow
            #  overriding instead of returning object below.
            return IntervalDtype(np.float64, closed=dtype.closed)
        return _dtype_obj
    elif dtype.kind == "b":
        return _dtype_obj
    elif dtype.kind in "iu":
        return np.dtype(np.float64)
    return dtype

