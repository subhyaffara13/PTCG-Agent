
def rindex(a, sub, start=0, end=None):
    """
    Like `rfind`, but raises :exc:`ValueError` when the substring `sub` is
    not found.

    Parameters
    ----------
    a : array-like, with ``bytes_`` or ``str_`` dtype

    sub : array-like, with ``bytes_`` or ``str_`` dtype

    start, end : array-like, with any integer dtype, optional

    Returns
    -------
    out : ndarray
        Output array of ints.

    See Also
    --------
    rfind, str.rindex

    Examples
    --------
    >>> a = np.array(["Computer Science"])
    >>> np.strings.rindex(a, "Science", start=0, end=None)
    array([9])

    """
    end = end if end is not None else MAX
    return _rindex_ufunc(a, sub, start, end)

