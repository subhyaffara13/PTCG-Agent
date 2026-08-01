
def is_nested_tuple(tup, labels) -> bool:
    """
    Returns
    -------
    bool
    """
    # check for a compatible nested tuple and multiindexes among the axes
    if not isinstance(tup, tuple):
        return False

    for k in tup:
        if is_list_like(k) or isinstance(k, slice):
            return isinstance(labels, MultiIndex)

    return False

