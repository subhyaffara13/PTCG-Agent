
def capitalize(s: str) -> str:
    """Capitalize the first character of a string."""
    if s == "":
        return ""
    else:
        return s[0].upper() + s[1:]


def capitalize(a):
    """
    Return a copy of ``a`` with only the first character of each element
    capitalized.

    Calls :meth:`str.capitalize` element-wise.

    For byte strings, this method is locale-dependent.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Input array of strings to capitalize.

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types

    See Also
    --------
    str.capitalize

    Examples
    --------
    >>> import numpy as np
    >>> c = np.array(['a1b2','1b2a','b2a1','2a1b'],'S4'); c
    array(['a1b2', '1b2a', 'b2a1', '2a1b'],
        dtype='|S4')
    >>> np.strings.capitalize(c)
    array(['A1b2', '1b2a', 'B2a1', '2a1b'],
        dtype='|S4')

    """
    a_arr = np.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'capitalize')

