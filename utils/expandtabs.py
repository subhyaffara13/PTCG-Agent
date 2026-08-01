
def expandtabs(a, tabsize=8):
    """
    Return a copy of each string element where all tab characters are
    replaced by one or more spaces.

    Calls :meth:`str.expandtabs` element-wise.

    Return a copy of each string element where all tab characters are
    replaced by one or more spaces, depending on the current column
    and the given `tabsize`. The column number is reset to zero after
    each newline occurring in the string. This doesn't understand other
    non-printing characters or escape sequences.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Input array
    tabsize : int, optional
        Replace tabs with `tabsize` number of spaces.  If not given defaults
        to 8 spaces.

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input type

    See Also
    --------
    str.expandtabs

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(['\t\tHello\tworld'])
    >>> np.strings.expandtabs(a, tabsize=4)  # doctest: +SKIP
    array(['        Hello   world'], dtype='<U21')  # doctest: +SKIP

    """
    a = np.asanyarray(a)
    tabsize = np.asanyarray(tabsize)

    if a.dtype.char == "T":
        return _expandtabs(a, tabsize)

    buffersizes = _expandtabs_length(a, tabsize)
    out_dtype = f"{a.dtype.char}{buffersizes.max()}"
    out = np.empty_like(a, shape=buffersizes.shape, dtype=out_dtype)
    return _expandtabs(a, tabsize, out=out)

