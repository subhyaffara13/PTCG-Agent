
def _get_datevalue(date, freq: BaseOffset):
    if isinstance(date, Period):
        return date.asfreq(freq).ordinal
    elif isinstance(date, (str, datetime, pydt.date, np.datetime64)):
        return Period(date, freq).ordinal  # pyright: ignore[reportAttributeAccessIssue]
    elif is_integer(date) or is_float(date):
        return date
    elif date is None:
        return None
    raise ValueError(f"Unrecognizable date '{date}'")

