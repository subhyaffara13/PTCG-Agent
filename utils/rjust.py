
def rjust(a, width, fillchar=' '):
    """
    Return an array with the elements of `a` right-justified in a
    string of length `width`.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype

    width : array_like, with any integer dtype
        The length of the resulting strings, unless ``width < str_len(a)``.
    fillchar : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Optional padding character to use (default is space).

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types

    See Also
    --------
    str.rjust

    Notes
    -----
    While it is possible for ``a`` and ``fillchar`` to have different dtypes,
    passing a non-ASCII character in ``fillchar`` when ``a`` is of dtype "S"
    is not allowed, and a ``ValueError`` is raised.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(['aAaAaA', '  aA  ', 'abBABba'])
    >>> np.strings.rjust(a, width=3)
    array(['aAaAaA', '  aA  ', 'abBABba'], dtype='<U7')
    >>> np.strings.rjust(a, width=9)
    array(['   aAaAaA', '     aA  ', '  abBABba'], dtype='<U9')

    """
    width = np.asanyarray(width)
    if not np.issubdtype(width.dtype, np.integer):
        raise TypeError(f"unsupported type {width.dtype} for operand 'width'")

    a = np.asanyarray(a)
    fillchar = np.asanyarray(fillchar)

    if np.any(str_len(fillchar) != 1):
        raise TypeError(
            "The fill character must be exactly one character long")

    if np.result_type(a, fillchar).char == "T":
        return _rjust(a, width, fillchar)

    fillchar = fillchar.astype(a.dtype, copy=False)
    width = np.maximum(str_len(a), width)
    shape = np.broadcast_shapes(a.shape, width.shape, fillchar.shape)
    out_dtype = f"{a.dtype.char}{width.max()}"
    out = np.empty_like(a, shape=shape, dtype=out_dtype)

    return _rjust(a, width, fillchar, out=out)

