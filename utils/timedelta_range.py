
def timedelta_range(
    start=None,
    end=None,
    periods: int | None = None,
    freq=None,
    name=None,
    closed=None,
    *,
    unit: TimeUnit | None = None,
) -> TimedeltaIndex:
    """
    Return a fixed frequency TimedeltaIndex with day as the default.

    Parameters
    ----------
    start : str or timedelta-like, default None
        Left bound for generating timedeltas.
    end : str or timedelta-like, default None
        Right bound for generating timedeltas.
    periods : int, default None
        Number of periods to generate.
    freq : str, Timedelta, datetime.timedelta, or DateOffset, default 'D'
        Frequency strings can have multiples, e.g. '5h'.
    name : Hashable, default None
        Name of the resulting TimedeltaIndex.
    closed : str, default None
        Make the interval closed with respect to the given frequency to
        the 'left', 'right', or both sides (None).
    unit : {'s', 'ms', 'us', 'ns', None}, default None
        Specify the desired resolution of the result.
        If not specified, this is inferred from the 'start', 'end', and 'freq'
        using the same inference as :class:`Timedelta` taking the highest
        resolution of the three that are provided.

        .. versionadded:: 2.0.0

    Returns
    -------
    TimedeltaIndex
        Fixed frequency, with day as the default.

    See Also
    --------
    date_range : Return a fixed frequency DatetimeIndex.
    period_range : Return a fixed frequency PeriodIndex.

    Notes
    -----
    Of the four parameters ``start``, ``end``, ``periods``, and ``freq``,
    a maximum of three can be specified at once. Of the three parameters
    ``start``, ``end``, and ``periods``, at least two must be specified.
    If ``freq`` is omitted, the resulting ``DatetimeIndex`` will have
    ``periods`` linearly spaced elements between ``start`` and ``end``
    (closed on both sides).

    To learn more about the frequency strings, please see
    :ref:`this link<timeseries.offset_aliases>`.

    Examples
    --------
    >>> pd.timedelta_range(start="1 day", periods=4)
    TimedeltaIndex(['1 days', '2 days', '3 days', '4 days'],
                   dtype='timedelta64[us]', freq='D')

    The ``closed`` parameter specifies which endpoint is included.  The default
    behavior is to include both endpoints.

    >>> pd.timedelta_range(start="1 day", periods=4, closed="right")
    TimedeltaIndex(['2 days', '3 days', '4 days'],
                   dtype='timedelta64[us]', freq='D')

    The ``freq`` parameter specifies the frequency of the TimedeltaIndex.
    Only fixed frequencies can be passed, non-fixed frequencies such as
    'M' (month end) will raise.

    >>> pd.timedelta_range(start="1 day", end="2 days", freq="6h")
    TimedeltaIndex(['1 days 00:00:00', '1 days 06:00:00', '1 days 12:00:00',
                    '1 days 18:00:00', '2 days 00:00:00'],
                   dtype='timedelta64[us]', freq='6h')

    Specify ``start``, ``end``, and ``periods``; the frequency is generated
    automatically (linearly spaced).

    >>> pd.timedelta_range(start="1 day", end="5 days", periods=4)
    TimedeltaIndex(['1 days 00:00:00', '2 days 08:00:00', '3 days 16:00:00',
                    '5 days 00:00:00'],
                   dtype='timedelta64[us]', freq=None)

    **Specify a unit**

    >>> pd.timedelta_range("1 Day", periods=3, freq="100000D", unit="s")
    TimedeltaIndex(['1 days', '100001 days', '200001 days'],
                   dtype='timedelta64[s]', freq='100000D')
    """
    if freq is None and com.any_none(periods, start, end):
        freq = "D"
    freq = to_offset(freq)

    if com.count_not_none(start, end, periods, freq) != 3:
        # This check needs to come before the `unit = start.unit` line below
        raise ValueError(
            "Of the four parameters: start, end, periods, "
            "and freq, exactly three must be specified"
        )

    if unit is None:
        # Infer the unit based on the inputs

        if start is not None and end is not None:
            start = Timedelta(start)
            end = Timedelta(end)
            start = cast(Timedelta, start)
            end = cast(Timedelta, end)
            if abbrev_to_npy_unit(start.unit) > abbrev_to_npy_unit(end.unit):
                unit = cast("TimeUnit", start.unit)
            else:
                unit = cast("TimeUnit", end.unit)
        elif start is not None:
            start = Timedelta(start)
            start = cast(Timedelta, start)
            unit = cast("TimeUnit", start.unit)
        else:
            end = Timedelta(end)
            end = cast(Timedelta, end)
            unit = cast("TimeUnit", end.unit)

        # Last we need to watch out for cases where the 'freq' implies a higher
        #  unit than either start or end
        if freq is not None:
            freq = cast("Tick | Day", freq)
            creso = abbrev_to_npy_unit(unit)
            if freq._creso > creso:  # pyright: ignore[reportAttributeAccessIssue]
                unit = cast("TimeUnit", freq.base.freqstr)

    tdarr = TimedeltaArray._generate_range(
        start, end, periods, freq, closed=closed, unit=unit
    )
    return TimedeltaIndex._simple_new(tdarr, name=name)

