
def objects_to_datetime64(
    data: np.ndarray,
    dayfirst,
    yearfirst,
    utc: bool = False,
    errors: DateTimeErrorChoices = "raise",
    allow_object: bool = False,
    out_unit: str | None = None,
) -> tuple[np.ndarray, tzinfo | None]:
    """
    Convert data to array of timestamps.

    Parameters
    ----------
    data : np.ndarray[object]
    dayfirst : bool
    yearfirst : bool
    utc : bool, default False
        Whether to convert/localize timestamps to UTC.
    errors : {'raise', 'coerce'}
    allow_object : bool
        Whether to return an object-dtype ndarray instead of raising if the
        data contains more than one timezone.
    out_unit : str or None, default None
        None indicates we should do resolution inference.

    Returns
    -------
    result : ndarray
        np.datetime64[out_unit] if returned values represent wall times or UTC
        timestamps.
        object if mixed timezones
    inferred_tz : tzinfo or None
        If not None, then the datetime64 values in `result` denote UTC timestamps.

    Raises
    ------
    ValueError : if data cannot be converted to datetimes
    TypeError  : When a type cannot be converted to datetime
    """
    assert errors in ["raise", "coerce"]

    # if str-dtype, convert
    data = np.asarray(data, dtype=np.object_)

    result, tz_parsed = tslib.array_to_datetime(
        data,
        errors=errors,
        utc=utc,
        dayfirst=dayfirst,
        yearfirst=yearfirst,
        creso=abbrev_to_npy_unit(out_unit),
    )

    if tz_parsed is not None:
        # We can take a shortcut since the datetime64 numpy array
        #  is in UTC
        return result, tz_parsed
    elif result.dtype.kind == "M":
        return result, tz_parsed
    elif result.dtype == object:
        # GH#23675 when called via `pd.to_datetime`, returning an object-dtype
        #  array is allowed.  When called via `pd.DatetimeIndex`, we can
        #  only accept datetime64 dtype, so raise TypeError if object-dtype
        #  is returned, as that indicates the values can be recognized as
        #  datetimes but they have conflicting timezones/awareness
        if allow_object:
            return result, tz_parsed
        raise TypeError("DatetimeIndex has mixed timezones")
    else:  # pragma: no cover
        # GH#23675 this TypeError should never be hit, whereas the TypeError
        #  in the object-dtype branch above is reachable.
        raise TypeError(result)

