
def _set_tz(
    values: npt.NDArray[np.int64], tz: str | tzinfo | None, datetime64_dtype: str
) -> DatetimeArray:
    """
    Coerce the values to a DatetimeArray with appropriate tz.

    Parameters
    ----------
    values : ndarray[int64]
    tz : str, tzinfo, or None
    datetime64_dtype : str, e.g. "datetime64[ns]", "datetime64[25s]"
    """
    assert values.dtype == "i8", values.dtype
    # Argument "tz" to "tz_to_dtype" has incompatible type "str | tzinfo | None";
    # expected "tzinfo"
    unit, _ = np.datetime_data(datetime64_dtype)  # parsing dtype: unit, count
    unit = cast("TimeUnit", unit)
    # error: Argument "tz" to "tz_to_dtype" has incompatible type
    #  "str | tzinfo | None"; expected "tzinfo"
    dtype = tz_to_dtype(tz=tz, unit=unit)  # type: ignore[arg-type]
    dta = DatetimeArray._from_sequence(values, dtype=dtype)
    return dta

