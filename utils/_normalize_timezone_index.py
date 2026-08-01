
def _normalize_timezone_index(index: pd.Index) -> pd.Index:
    if isinstance(index, pd.MultiIndex):
        if any(isinstance(level.dtype, pd.DatetimeTZDtype) for level in index.levels):
            levels = [_normalize_timezone_index(level) for level in index.levels]
            return index.set_levels(levels)

        return index

    if isinstance(index.dtype, pd.DatetimeTZDtype):
        normalized_tz = _normalize_pytz_timezone(index.dtype.tz)
        if normalized_tz is not index.dtype.tz:
            return index.tz_convert(normalized_tz)  # type: ignore[attr-defined]

    return index

