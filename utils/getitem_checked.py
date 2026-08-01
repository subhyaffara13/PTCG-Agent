
def getitem_checked(mapping, /, _error_cls=ValueError, **kwargs):
    """
    *kwargs* must consist of a single *key, value* pair.  If *key* is in
    *mapping*, return ``mapping[value]``; else, raise an appropriate
    ValueError.

    Parameters
    ----------
    _error_cls :
        Class of error to raise.

    Examples
    --------
    >>> _api.getitem_checked({"foo": "bar"}, arg=arg)
    """
    if len(kwargs) != 1:
        raise ValueError("getitem_checked takes a single keyword argument")
    (k, v), = kwargs.items()
    try:
        return mapping[v]
    except KeyError:
        raise _error_cls(list_suggestion_error_msg(k, v, mapping.keys())) from None

