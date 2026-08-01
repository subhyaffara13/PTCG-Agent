
def _adjust_dates_anchored(
    first: Timestamp,
    last: Timestamp,
    freq: Tick,
    closed: Literal["right", "left"] = "right",
    origin: TimeGrouperOrigin = "start_day",
    offset: Timedelta | None = None,
    unit: TimeUnit = "ns",
) -> tuple[Timestamp, Timestamp]:
    # First and last offsets should be calculated from the start day to fix an
    # error cause by resampling across multiple days when a one day period is
    # not a multiple of the frequency. See GH 8683
    # To handle frequencies that are not multiple or divisible by a day we let
    # the possibility to define a fixed origin timestamp. See GH 31809
    first = first.as_unit(unit)
    last = last.as_unit(unit)
    if offset is not None:
        offset = offset.as_unit(unit)

    freq_value = Timedelta(freq).as_unit(unit)._value

    origin_timestamp = 0  # origin == "epoch"
    if origin == "start_day":
        origin_timestamp = first.normalize()._value
    elif origin == "start":
        origin_timestamp = first._value
    elif isinstance(origin, Timestamp):
        origin_timestamp = origin.as_unit(unit)._value
    elif origin in ["end", "end_day"]:
        origin_last = last if origin == "end" else last.ceil("D")
        sub_freq_times = (origin_last._value - first._value) // freq_value
        if closed == "left":
            sub_freq_times += 1
        first = origin_last - sub_freq_times * freq
        origin_timestamp = first._value
    origin_timestamp += offset._value if offset else 0

    # GH 10117 & GH 19375. If first and last contain timezone information,
    # Perform the calculation in UTC in order to avoid localizing on an
    # Ambiguous or Nonexistent time.
    first_tzinfo = first.tzinfo
    last_tzinfo = last.tzinfo
    if first_tzinfo is not None:
        first = first.tz_convert("UTC")
    if last_tzinfo is not None:
        last = last.tz_convert("UTC")

    foffset = (first._value - origin_timestamp) % freq_value
    loffset = (last._value - origin_timestamp) % freq_value

    if closed == "right":
        if foffset > 0:
            # roll back
            fresult_int = first._value - foffset
        else:
            fresult_int = first._value - freq_value

        if loffset > 0:
            # roll forward
            lresult_int = last._value + (freq_value - loffset)
        else:
            # already the end of the road
            lresult_int = last._value
    else:  # closed == 'left'
        if foffset > 0:
            fresult_int = first._value - foffset
        else:
            # start of the road
            fresult_int = first._value

        if loffset > 0:
            # roll forward
            lresult_int = last._value + (freq_value - loffset)
        else:
            lresult_int = last._value + freq_value
    fresult = Timestamp(fresult_int, unit=unit)
    lresult = Timestamp(lresult_int, unit=unit)
    if first_tzinfo is not None:
        fresult = fresult.tz_localize("UTC").tz_convert(first_tzinfo)
    if last_tzinfo is not None:
        lresult = lresult.tz_localize("UTC").tz_convert(last_tzinfo)
    return fresult, lresult

