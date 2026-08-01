
def rpartition(a, sep):
    """
    Partition (split) each element around the right-most separator.

    Calls :meth:`str.rpartition` element-wise.

    For each element in `a`, split the element as the last
    occurrence of `sep`, and return 3 strings containing the part
    before the separator, the separator itself, and the part after
    the separator. If the separator is not found, return 3 strings
    containing the string itself, followed by two empty strings.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Input array
    sep : str or unicode
        Right-most separator to split each element in array.

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types. The output array will have an extra
        dimension with 3 elements per input element.

    See Also
    --------
    str.rpartition

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(['aAaAaA', '  aA  ', 'abBABba'])
    >>> np.char.rpartition(a, 'A')
    array([['aAaAa', 'A', ''],
       ['  a', 'A', '  '],
       ['abB', 'A', 'Bba']], dtype='<U5')

    """
    return np.stack(strings_rpartition(a, sep), axis=-1)


def rpartition(a, sep):
    """
    Partition (split) each element around the right-most separator.

    For each element in ``a``, split the element at the last
    occurrence of ``sep``, and return a 3-tuple containing the part
    before the separator, the separator itself, and the part after
    the separator. If the separator is not found, the third item of
    the tuple will contain the whole string, and the first and second
    ones will be the empty string.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Input array
    sep : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Separator to split each string element in ``a``.

    Returns
    -------
    out : 3-tuple:
        - array with ``StringDType``, ``bytes_`` or ``str_`` dtype with the
          part before the separator
        - array with ``StringDType``, ``bytes_`` or ``str_`` dtype with the
          separator
        - array with ``StringDType``, ``bytes_`` or ``str_`` dtype with the
          part after the separator

    See Also
    --------
    str.rpartition

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(['aAaAaA', '  aA  ', 'abBABba'])
    >>> np.strings.rpartition(a, 'A')
    (array(['aAaAa', '  a', 'abB'], dtype='<U5'),
     array(['A', 'A', 'A'], dtype='<U1'),
     array(['', '  ', 'Bba'], dtype='<U3'))

    """
    a = np.asanyarray(a)
    sep = np.asanyarray(sep)

    if np.result_type(a, sep).char == "T":
        return _rpartition(a, sep)

    sep = sep.astype(a.dtype, copy=False)
    pos = _rfind_ufunc(a, sep, 0, MAX)
    a_len = str_len(a)
    sep_len = str_len(sep)

    not_found = pos < 0
    buffersizes1 = np.where(not_found, 0, pos)
    buffersizes3 = np.where(not_found, a_len, a_len - pos - sep_len)

    out_dtype = ",".join([f"{a.dtype.char}{n}" for n in (
        buffersizes1.max(),
        1 if np.all(not_found) else sep_len.max(),
        buffersizes3.max(),
    )])
    shape = np.broadcast_shapes(a.shape, sep.shape)
    out = np.empty_like(a, shape=shape, dtype=out_dtype)
    return _rpartition_index(
        a, sep, pos, out=(out["f0"], out["f1"], out["f2"]))

