
def _array_strptime_with_fallback(
    arg,
    name,
    utc: bool,
    fmt: str,
    exact: bool,
    errors: str,
) -> Index:
    """
    Call array_strptime, with fallback behavior depending on 'errors'.
    """
    result, tz_out = array_strptime(arg, fmt, exact=exact, errors=errors, utc=utc)
    if tz_out is not None:
        unit = np.datetime_data(result.dtype)[0]
        unit = cast("TimeUnit", unit)
        dtype = DatetimeTZDtype(tz=tz_out, unit=unit)
        dta = DatetimeArray._simple_new(result, dtype=dtype)
        if utc:
            dta = dta.tz_convert("UTC")
        return Index(dta, name=name, copy=False)
    elif result.dtype != object and utc:
        unit = np.datetime_data(result.dtype)[0]
        unit = cast("TimeUnit", unit)
        res = Index(result, dtype=f"M8[{unit}, UTC]", name=name, copy=False)
        return res
    return Index(result, dtype=result.dtype, name=name, copy=False)

