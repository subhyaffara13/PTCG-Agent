
def lower(a):
    """
    Return an array with the elements converted to lowercase.

    Call :meth:`str.lower` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Input array.

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types

    See Also
    --------
    str.lower

    Examples
    --------
    >>> import numpy as np
    >>> c = np.array(['A1B C', '1BCA', 'BCA1']); c
    array(['A1B C', '1BCA', 'BCA1'], dtype='<U5')
    >>> np.strings.lower(c)
    array(['a1b c', '1bca', 'bca1'], dtype='<U5')

    """
    a_arr = np.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'lower')


def lower(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()

