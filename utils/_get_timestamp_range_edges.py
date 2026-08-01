
def _get_timestamp_range_edges(
    first: Timestamp,
    last: Timestamp,
    freq: BaseOffset,
    unit: TimeUnit,
    closed: Literal["right", "left"] = "left",
    origin: TimeGrouperOrigin = "start_day",
    offset: Timedelta | None = None,
) -> tuple[Timestamp, Timestamp]:
    """
    Adjust the `first` Timestamp to the preceding Timestamp that resides on
    the provided offset. Adjust the `last` Timestamp to the following
    Timestamp that resides on the provided offset. Input Timestamps that
    already reside on the offset will be adjusted depending on the type of
    offset and the `closed` parameter.

    Parameters
    ----------
    first : pd.Timestamp
        The beginning Timestamp of the range to be adjusted.
    last : pd.Timestamp
        The ending Timestamp of the range to be adjusted.
    freq : pd.DateOffset
        The dateoffset to which the Timestamps will be adjusted.
    closed : {'right', 'left'}, default "left"
        Which side of bin interval is closed.
    origin : {'epoch', 'start', 'start_day'} or Timestamp, default 'start_day'
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
    A tuple of length 2, containing the adjusted pd.Timestamp objects.
    """
    if isinstance(freq, Tick):
        index_tz = first.tz
        if isinstance(origin, Timestamp) and (origin.tz is None) != (index_tz is None):
            raise ValueError("The origin must have the same timezone as the index.")
        if origin == "epoch":
            # set the epoch based on the timezone to have similar bins results when
            # resampling on the same kind of indexes on different timezones
            origin = Timestamp("1970-01-01", tz=index_tz)

        first, last = _adjust_dates_anchored(
            first,
            last,
            freq,
            closed=closed,
            origin=origin,
            offset=offset,
            unit=unit,
        )
    else:
        first = first.normalize()
        last = last.normalize()

        if closed == "left":
            first = Timestamp(freq.rollback(first))
        else:
            first = Timestamp(first - freq)

        last = Timestamp(last + freq)

    return first, last

