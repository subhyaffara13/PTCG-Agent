
def recursive_fill_fields(input, output):
    """
    Fills fields from output with fields from input,
    with support for nested structures.

    Parameters
    ----------
    input : ndarray
        Input array.
    output : ndarray
        Output array.

    Notes
    -----
    * `output` should be at least the same size as `input`

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.lib import recfunctions as rfn
    >>> a = np.array([(1, 10.), (2, 20.)], dtype=[('A', np.int64), ('B', np.float64)])
    >>> b = np.zeros((3,), dtype=a.dtype)
    >>> rfn.recursive_fill_fields(a, b)
    array([(1, 10.), (2, 20.), (0,  0.)], dtype=[('A', '<i8'), ('B', '<f8')])

    """
    newdtype = output.dtype
    for field in newdtype.names:
        try:
            current = input[field]
        except ValueError:
            continue
        if current.dtype.names is not None:
            recursive_fill_fields(current, output[field])
        else:
            output[field][:len(current)] = current
    return output

