
def _validate_usecols_arg(usecols):
    """
    Validate the 'usecols' parameter.

    Checks whether or not the 'usecols' parameter contains all integers
    (column selection by index), strings (column by name) or is a callable.
    Raises a ValueError if that is not the case.

    Parameters
    ----------
    usecols : list-like, callable, or None
        List of columns to use when parsing or a callable that can be used
        to filter a list of table columns.

    Returns
    -------
    usecols_tuple : tuple
        A tuple of (verified_usecols, usecols_dtype).

        'verified_usecols' is either a set if an array-like is passed in or
        'usecols' if a callable or None is passed in.

        'usecols_dtype` is the inferred dtype of 'usecols' if an array-like
        is passed in or None if a callable or None is passed in.
    """
    msg = (
        "'usecols' must either be list-like of all strings, all unicode, "
        "all integers or a callable."
    )
    if usecols is not None:
        if callable(usecols):
            return usecols, None

        if not is_list_like(usecols):
            # see gh-20529
            #
            # Ensure it is iterable container but not string.
            raise ValueError(msg)

        usecols_dtype = lib.infer_dtype(usecols, skipna=False)

        if usecols_dtype not in ("empty", "integer", "string"):
            raise ValueError(msg)

        usecols = set(usecols)

        return usecols, usecols_dtype
    return usecols, None

