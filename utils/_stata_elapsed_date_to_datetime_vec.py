
def _stata_elapsed_date_to_datetime_vec(dates: Series, fmt: str) -> Series:
    """
    Convert from SIF to datetime. https://www.stata.com/help.cgi?datetime

    Parameters
    ----------
    dates : Series
        The Stata Internal Format date to convert to datetime according to fmt
    fmt : str
        The format to convert to. Can be, tc, td, tw, tm, tq, th, ty
        Returns

    Returns
    -------
    converted : Series
        The converted dates

    Examples
    --------
    >>> dates = pd.Series([52])
    >>> _stata_elapsed_date_to_datetime_vec(dates, "%tw")
    0   1961-01-01
    dtype: datetime64[s]

    Notes
    -----
    datetime/c - tc
        milliseconds since 01jan1960 00:00:00.000, assuming 86,400 s/day
    datetime/C - tC - NOT IMPLEMENTED
        milliseconds since 01jan1960 00:00:00.000, adjusted for leap seconds
    date - td
        days since 01jan1960 (01jan1960 = 0)
    weekly date - tw
        weeks since 1960w1
        This assumes 52 weeks in a year, then adds 7 * remainder of the weeks.
        The datetime value is the start of the week in terms of days in the
        year, not ISO calendar weeks.
    monthly date - tm
        months since 1960m1
    quarterly date - tq
        quarters since 1960q1
    half-yearly date - th
        half-years since 1960h1 yearly
    date - ty
        years since 0000
    """

    if fmt.startswith(("%tc", "tc")):
        # Delta ms relative to base
        td = np.timedelta64(stata_epoch - unix_epoch, "ms")
        res = np.array(dates._values, dtype="M8[ms]") + td
        return Series(res, index=dates.index)

    elif fmt.startswith(("%td", "td", "%d", "d")):
        # Delta days relative to base
        td = np.timedelta64(stata_epoch - unix_epoch, "D")
        res = np.array(dates._values, dtype="M8[D]") + td
        return Series(res, index=dates.index)

    elif fmt.startswith(("%tm", "tm")):
        # Delta months relative to base
        ordinals = dates + (stata_epoch.year - unix_epoch.year) * 12
        res = np.array(ordinals, dtype="M8[M]").astype("M8[s]")
        return Series(res, index=dates.index)

    elif fmt.startswith(("%tq", "tq")):
        # Delta quarters relative to base
        ordinals = dates + (stata_epoch.year - unix_epoch.year) * 4
        res = np.array(ordinals, dtype="M8[3M]").astype("M8[s]")
        return Series(res, index=dates.index)

    elif fmt.startswith(("%th", "th")):
        # Delta half-years relative to base
        ordinals = dates + (stata_epoch.year - unix_epoch.year) * 2
        res = np.array(ordinals, dtype="M8[6M]").astype("M8[s]")
        return Series(res, index=dates.index)

    elif fmt.startswith(("%ty", "ty")):
        # Years -- not delta
        ordinals = dates - 1970
        res = np.array(ordinals, dtype="M8[Y]").astype("M8[s]")
        return Series(res, index=dates.index)

    bad_locs = np.isnan(dates)
    has_bad_values = False
    if bad_locs.any():
        has_bad_values = True
        dates._values[bad_locs] = 1.0  # Replace with NaT
    dates = dates.astype(np.int64)

    if fmt.startswith(("%tC", "tC")):
        warnings.warn(
            "Encountered %tC format. Leaving in Stata Internal Format.",
            stacklevel=find_stack_level(),
        )
        conv_dates = Series(dates, dtype=object)
        if has_bad_values:
            conv_dates[bad_locs] = NaT
        return conv_dates
    # does not count leap days - 7 days is a week.
    # 52nd week may have more than 7 days
    elif fmt.startswith(("%tw", "tw")):
        year = stata_epoch.year + dates // 52
        days = (dates % 52) * 7
        per_y = (year - 1970).array.view("Period[Y]")
        per_d = per_y.asfreq("D", how="S")
        per_d_shifted = per_d + days._values
        per_s = per_d_shifted.asfreq("s", how="S")
        conv_dates_arr = per_s.view("M8[s]")
        conv_dates = Series(conv_dates_arr, index=dates.index)

    else:
        raise ValueError(f"Date fmt {fmt} not understood")

    if has_bad_values:  # Restore NaT for bad values
        conv_dates[bad_locs] = NaT

    return conv_dates

