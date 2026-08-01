
def _rsplit(a, sep=None, maxsplit=None):
    """
    For each element in `a`, return a list of the words in the
    string, using `sep` as the delimiter string.

    Calls :meth:`str.rsplit` element-wise.

    Except for splitting from the right, `rsplit`
    behaves like `split`.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype

    sep : str or unicode, optional
        If `sep` is not specified or None, any whitespace string
        is a separator.
    maxsplit : int, optional
        If `maxsplit` is given, at most `maxsplit` splits are done,
        the rightmost ones.

    Returns
    -------
    out : ndarray
        Array of list objects

    See Also
    --------
    str.rsplit, split

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(['aAaAaA', 'abBABba'])
    >>> np.strings.rsplit(a, 'A')  # doctest: +SKIP
    array([list(['a', 'a', 'a', '']),  # doctest: +SKIP
           list(['abB', 'Bba'])], dtype=object)  # doctest: +SKIP

    """
    # This will return an array of lists of different sizes, so we
    # leave it as an object array
    return _vec_string(
        a, np.object_, 'rsplit', [sep] + _clean_args(maxsplit))

