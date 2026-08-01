
def _normalize_timezone_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    PyArrow uses pytz by default for timezones, but pandas uses
    zoneinfo / datetime.timezone since pandas 3.0.

    TODO: Starting with pyarrow 25, it will use zoneinfo by default, and then
    this normalization can be skipped (https://github.com/apache/arrow/pull/49694).
    """
    if pytz is not None:
        # Convert any pytz timezones to zoneinfo / fixed offset timezones
        if any(
            isinstance(dtype, pd.DatetimeTZDtype)
            for dtype in df._mgr.get_unique_dtypes()
        ):
            col_indices = df._select_dtypes_indices(pd.DatetimeTZDtype)
            for i in col_indices:
                col = df.iloc[:, i]
                normalized_tz = _normalize_pytz_timezone(col.dtype.tz)
                if normalized_tz is not col.dtype.tz:
                    df.isetitem(i, col.dt.tz_convert(normalized_tz))

        df.index = _normalize_timezone_index(df.index)
        df.columns = _normalize_timezone_index(df.columns)

    return df

