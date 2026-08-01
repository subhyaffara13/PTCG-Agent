
def _get_period_range_edges(
    first: Period,
    last: Period,
    freq: BaseOffset,
    closed: Literal["right", "left"] = "left",
    origin: TimeGrouperOrigin = "start_day",
    offset: Timedelta | None = None,
) -> tuple[Period, Period]:
    """
    Adjust the provided `first` and `last` Periods to the respective Period of
    the given offset that encompasses them.

    Parameters
    ----------
    first : pd.Period
        The beginning Period of the range to be adjusted.
    last : pd.Period
        The ending Period of the range to be adjusted.
    freq : pd.DateOffset
        The freq to which the Periods will be adjusted.
    closed : {'right', 'left'}, default "left"
        Which side of bin interval is closed.
    origin : {'epoch', 'start', 'start_day'}, Timestamp, default 'start_day'
        The timestamp on which to adjust the grouping. The timezone of origin must
        match the timezone of the index.

        If a timestamp is not used, these values are also supported:

        - 'epoch': `origin` is 1970-01-01
        - 'start': `origin` is the first value of the timeseries
        - 'start_day': `origin` is the first day at midnight of the timeseries
    offset : pd.Timedelta, default is None
        An offset timedelta added to the origin.

    Returns
    -------
    A tuple of length 2, containing the adjusted pd.Period objects.
    """
    if not all(isinstance(obj, Period) for obj in [first, last]):
        raise TypeError("'first' and 'last' must be instances of type Period")

    # GH 23882
    first_ts = first.to_timestamp()
    last_ts = last.to_timestamp()
    adjust_first = not freq.is_on_offset(first_ts)
    adjust_last = freq.is_on_offset(last_ts)

    first_ts, last_ts = _get_timestamp_range_edges(
        first_ts, last_ts, freq, unit="ns", closed=closed, origin=origin, offset=offset
    )

    first = (first_ts + int(adjust_first) * freq).to_period(freq)
    last = (last_ts - int(adjust_last) * freq).to_period(freq)
    return first, last

