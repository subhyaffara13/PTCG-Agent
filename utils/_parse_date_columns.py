
def _parse_date_columns(data_frame: DataFrame, parse_dates) -> DataFrame:
    """
    Force non-datetime columns to be read as such.
    Supports both string formatted and integer timestamp columns.
    """
    parse_dates = _process_parse_dates_argument(parse_dates)

    # we want to coerce datetime64_tz dtypes for now to UTC
    # we could in theory do a 'nice' conversion from a FixedOffset tz
    # GH11216
    for i, (col_name, df_col) in enumerate(data_frame.items()):
        if isinstance(df_col.dtype, DatetimeTZDtype) or col_name in parse_dates:
            try:
                fmt = parse_dates[col_name]
            except (KeyError, TypeError):
                fmt = None
            data_frame.isetitem(i, _handle_date_column(df_col, format=fmt))

    return data_frame

