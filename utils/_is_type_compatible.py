
def _is_type_compatible(a, b) -> bool:
    """
    Helper for interval_range to check type compat of start/end/freq.
    """
    is_ts_compat = lambda x: isinstance(x, (Timestamp, BaseOffset))
    is_td_compat = lambda x: isinstance(x, (Timedelta, BaseOffset))
    return (
        (is_number(a) and is_number(b))
        or (is_ts_compat(a) and is_ts_compat(b))
        or (is_td_compat(a) and is_td_compat(b))
        or com.any_none(a, b)
    )

