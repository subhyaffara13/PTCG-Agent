
def fill_missing_names(names: Sequence[Hashable | None]) -> list[Hashable]:
    """
    If a name is missing then replace it by level_n, where n is the count

    Parameters
    ----------
    names : list-like
        list of column names or None values.

    Returns
    -------
    list
        list of column names with the None values replaced.
    """
    return [f"level_{i}" if name is None else name for i, name in enumerate(names)]

