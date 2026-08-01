
def _get_fill_value(
    dtype: DtypeObj, fill_value: Scalar | None = None, fill_value_typ=None
):
    """return the correct fill value for the dtype of the values"""
    if fill_value is not None:
        return fill_value
    if _na_ok_dtype(dtype):
        if fill_value_typ is None:
            return np.nan
        elif fill_value_typ == "+inf":
            return np.inf
        else:
            return -np.inf
    elif fill_value_typ == "+inf":
        # need the max int here
        # Return as np.int64 so that np.where promotes the dtype
        # instead of raising OverflowError (numpy 2.5+) when the
        # value doesn't fit in the array's dtype (e.g. int8).
        return np.int64(lib.i8max)
    else:
        return np.int64(iNaT)

