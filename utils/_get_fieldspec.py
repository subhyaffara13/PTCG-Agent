
def _get_fieldspec(dtype):
    """
    Produce a list of name/dtype pairs corresponding to the dtype fields

    Similar to dtype.descr, but the second item of each tuple is a dtype, not a
    string. As a result, this handles subarray dtypes

    Can be passed to the dtype constructor to reconstruct the dtype, noting that
    this (deliberately) discards field offsets.

    Examples
    --------
    >>> import numpy as np
    >>> dt = np.dtype([(('a', 'A'), np.int64), ('b', np.double, 3)])
    >>> dt.descr
    [(('a', 'A'), '<i8'), ('b', '<f8', (3,))]
    >>> _get_fieldspec(dt)
    [(('a', 'A'), dtype('int64')), ('b', dtype(('<f8', (3,))))]

    """
    if dtype.names is None:
        # .descr returns a nameless field, so we should too
        return [('', dtype)]
    else:
        fields = ((name, dtype.fields[name]) for name in dtype.names)
        # keep any titles, if present
        return [
            (name if len(f) == 2 else (f[2], name), f[0])
            for name, f in fields
        ]

