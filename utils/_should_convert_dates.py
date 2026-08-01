
def _should_convert_dates(
    convert_dates: bool | list[str],
    keep_default_dates: bool,
    col: Hashable,
) -> bool:
    """
    Return bool whether a DataFrame column should be cast to datetime.
    """
    if convert_dates is False:
        # convert_dates=True means follow keep_default_dates
        return False
    elif not isinstance(convert_dates, bool) and col in set(convert_dates):
        return True
    elif not keep_default_dates:
        return False
    elif not isinstance(col, str):
        return False
    col_lower = col.lower()
    if (
        col_lower.endswith(("_at", "_time"))
        or col_lower in {"modified", "date", "datetime"}
        or col_lower.startswith("timestamp")
    ):
        return True
    return False

