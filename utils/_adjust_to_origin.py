
def _adjust_to_origin(arg, origin, unit):
    """
    Helper function for to_datetime.
    Adjust input argument to the specified origin

    Parameters
    ----------
    arg : list, tuple, ndarray, Series, Index
        date to be adjusted
    origin : 'julian' or Timestamp
        origin offset for the arg
    unit : str
        passed unit from to_datetime, must be 'D'

    Returns
    -------
    ndarray or scalar of adjusted date(s)
    """
    if origin == "julian":
        original = arg
        j0 = Timestamp(0).to_julian_date()
        if unit != "D":
            raise ValueError("unit must be 'D' for origin='julian'")
        try:
            arg = arg - j0
        except TypeError as err:
            raise ValueError(
                "incompatible 'arg' type for given 'origin'='julian'"
            ) from err

        # preemptively check this for a nice range
        j_max = Timestamp.max.to_julian_date() - j0
        j_min = Timestamp.min.to_julian_date() - j0
        if np.any(arg > j_max) or np.any(arg < j_min):
            raise OutOfBoundsDatetime(
                f"{original} is Out of Bounds for origin='julian'"
            )
    else:
        # arg must be numeric
        if not (
            (is_integer(arg) or is_float(arg)) or is_numeric_dtype(np.asarray(arg))
        ):
            raise ValueError(
                f"'{arg}' is not compatible with origin='{origin}'; "
                "it must be numeric with a unit specified"
            )

        # we are going to offset back to unix / epoch time
        try:
            if lib.is_integer(origin) or lib.is_float(origin):
                offset = Timestamp(origin, unit=unit)
            else:
                offset = Timestamp(origin)
        except OutOfBoundsDatetime as err:
            raise OutOfBoundsDatetime(f"origin {origin} is Out of Bounds") from err
        except ValueError as err:
            raise ValueError(
                f"origin {origin} cannot be converted to a Timestamp"
            ) from err

        if offset.tz is not None:
            raise ValueError(f"origin offset {offset} must be tz-naive")
        td_offset = offset - Timestamp(0)

        # convert the offset to the unit of the arg
        # this should be lossless in terms of precision
        ioffset = td_offset // Timedelta(1, unit=unit)

        # scalars & ndarray-like can handle the addition
        if is_list_like(arg) and not isinstance(arg, (ABCSeries, Index, np.ndarray)):
            arg = np.asarray(arg)
        arg = arg + ioffset
    return arg

