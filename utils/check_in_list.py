
def check_in_list(values, /, **kwargs):
    """
    For each *key, value* pair in *kwargs*, check that *value* is in *values*;
    if not, raise an appropriate ValueError.

    Parameters
    ----------
    values : iterable
        Sequence of values to check on.

        Note: All values must support == comparisons.
        This means in particular the entries must not be numpy arrays.
    **kwargs : dict
        *key, value* pairs as keyword arguments to find in *values*.

    Raises
    ------
    ValueError
        If any *value* in *kwargs* is not found in *values*.

    Examples
    --------
    >>> _api.check_in_list(["foo", "bar"], arg=arg, other_arg=other_arg)
    """
    if not kwargs:
        raise TypeError("No argument to check!")
    for key, val in kwargs.items():
        try:
            exists = val in values
        except ValueError:
            # `in` internally uses `val == values[i]`. There are some objects
            # that do not support == to arbitrary other objects, in particular
            # numpy arrays.
            # Since such objects are not allowed in values, we can gracefully
            # handle the case that val (typically provided by users) is of such
            # type and directly state it's not in the list instead of letting
            # the individual `val == values[i]` ValueError surface.
            exists = False
        if not exists:
            raise ValueError(list_suggestion_error_msg(key, val, values))

