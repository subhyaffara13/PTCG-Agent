
def _join(sep, seq):
    """
    Return a string which is the concatenation of the strings in the
    sequence `seq`.

    Calls :meth:`str.join` element-wise.

    Parameters
    ----------
    sep : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
    seq : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types

    See Also
    --------
    str.join

    Examples
    --------
    >>> import numpy as np
    >>> np.strings.join('-', 'osd')  # doctest: +SKIP
    array('o-s-d', dtype='<U5')  # doctest: +SKIP

    >>> np.strings.join(['-', '.'], ['ghc', 'osd'])  # doctest: +SKIP
    array(['g-h-c', 'o.s.d'], dtype='<U5')  # doctest: +SKIP

    """
    return _to_bytes_or_str_array(
        _vec_string(sep, np.object_, 'join', (seq,)), seq)

