
def _splitlines(a, keepends=None):
    """
    For each element in `a`, return a list of the lines in the
    element, breaking at line boundaries.

    Calls :meth:`str.splitlines` element-wise.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype

    keepends : bool, optional
        Line breaks are not included in the resulting list unless
        keepends is given and true.

    Returns
    -------
    out : ndarray
        Array of list objects

    See Also
    --------
    str.splitlines

    Examples
    --------
    >>> np.char.splitlines("first line\\nsecond line")
    array(list(['first line', 'second line']), dtype=object)
    >>> a = np.array(["first\\nsecond", "third\\nfourth"])
    >>> np.char.splitlines(a)
    array([list(['first', 'second']), list(['third', 'fourth'])], dtype=object)

    """
    return _vec_string(
        a, np.object_, 'splitlines', _clean_args(keepends))

