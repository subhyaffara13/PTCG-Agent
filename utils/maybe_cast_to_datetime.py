
def maybe_cast_to_datetime(
    value: np.ndarray | list, dtype: np.dtype
) -> DatetimeArray | TimedeltaArray | np.ndarray:
    """
    try to cast the array/value to a datetimelike dtype, converting float
    nan to iNaT

    Caller is responsible for handling ExtensionDtype cases and non dt64/td64
    cases.
    """
    from pandas.core.arrays.datetimes import DatetimeArray
    from pandas.core.arrays.timedeltas import TimedeltaArray

    assert dtype.kind in "mM"
    if not is_list_like(value):
        raise TypeError("value must be listlike")

    # TODO: _from_sequence would raise ValueError in cases where
    #  _ensure_nanosecond_dtype raises TypeError
    _ensure_nanosecond_dtype(dtype)

    if lib.is_np_dtype(dtype, "m"):
        res = TimedeltaArray._from_sequence(value, dtype=dtype)
        return res
    else:
        try:
            dta = DatetimeArray._from_sequence(value, dtype=dtype)
        except ValueError as err:
            # We can give a Series-specific exception message.
            if "cannot supply both a tz and a timezone-naive dtype" in str(err):
                raise ValueError(
                    "Cannot convert timezone-aware data to "
                    "timezone-naive dtype. Use "
                    "pd.Series(values).dt.tz_localize(None) instead."
                ) from err
            raise

        return dta

