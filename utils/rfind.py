
def rfind(a, sub, start=0, end=None):
    """
    For each element, return the highest index in the string where
    substring ``sub`` is found, such that ``sub`` is contained in the
    range [``start``, ``end``).

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype

    sub : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        The substring to search for.

    start, end : array_like, with any integer dtype
        The range to look in, interpreted as in slice notation.

    Returns
    -------
    y : ndarray
        Output array of ints

    See Also
    --------
    str.rfind

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(["Computer Science"])
    >>> np.strings.rfind(a, "Science", start=0, end=None)
    array([9])
    >>> np.strings.rfind(a, "Science", start=0, end=8)
    array([-1])
    >>> b = np.array(["Computer Science", "Science"])
    >>> np.strings.rfind(b, "Science", start=0, end=None)
    array([9, 0])

    """
    end = end if end is not None else MAX
    return _rfind_ufunc(a, sub, start, end)

