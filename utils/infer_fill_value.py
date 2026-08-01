
def infer_fill_value(val):
    """
    infer the fill value for the nan/NaT from the provided
    scalar/ndarray/list-like if we are a NaT, return the correct dtyped
    element to provide proper block construction
    """
    if not is_list_like(val):
        val = [val]
    val = np.asarray(val)
    if val.dtype.kind in "mM":
        return np.array("NaT", dtype=val.dtype)
    elif val.dtype == object:
        dtype = lib.infer_dtype(ensure_object(val), skipna=False)
        if dtype in ["datetime", "datetime64"]:
            return np.array("NaT", dtype=DT64NS_DTYPE)
        elif dtype in ["timedelta", "timedelta64"]:
            return np.array("NaT", dtype=TD64NS_DTYPE)
        return np.array(np.nan, dtype=object)
    elif val.dtype.kind == "U":
        return np.array(np.nan, dtype=val.dtype)
    return np.nan

