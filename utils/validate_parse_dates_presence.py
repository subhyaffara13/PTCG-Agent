
def validate_parse_dates_presence(
    parse_dates: bool | list, columns: Sequence[Hashable]
) -> set:
    """
    Check if parse_dates are in columns.

    If user has provided names for parse_dates, check if those columns
    are available.

    Parameters
    ----------
    columns : list
        List of names of the dataframe.

    Returns
    -------
    The names of the columns which will get parsed later if a list
    is given as specification.

    Raises
    ------
    ValueError
        If column to parse_date is not in dataframe.

    """
    if not isinstance(parse_dates, list):
        return set()

    missing = set()
    unique_cols = set()
    for col in parse_dates:
        if isinstance(col, str):
            if col not in columns:
                missing.add(col)
            else:
                unique_cols.add(col)
        elif col in columns:
            unique_cols.add(col)
        else:
            unique_cols.add(columns[col])
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"Missing column provided to 'parse_dates': '{missing_cols}'")
    return unique_cols

