
def date_converter(
    date_col,
    col: Hashable,
    dayfirst: bool = False,
    cache_dates: bool = True,
    date_format: dict[Hashable, str] | str | None = None,
):
    if date_col.dtype.kind in "Mm":
        return date_col

    date_fmt = date_format.get(col) if isinstance(date_format, dict) else date_format

    str_objs = lib.ensure_string_array(np.asarray(date_col))
    try:
        result = tools.to_datetime(
            str_objs,
            format=date_fmt,
            utc=False,
            dayfirst=dayfirst,
            cache=cache_dates,
        )
    except (ValueError, TypeError):
        # test_usecols_with_parse_dates4
        # test_multi_index_parse_dates
        return str_objs

    if isinstance(result, DatetimeIndex):
        arr = result.to_numpy()
        arr.flags.writeable = True
        return arr
    return result._values

