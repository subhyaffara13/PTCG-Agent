
def common_fill_value(a, b):
    """
    Return the common filling value of two masked arrays, if any.

    If ``a.fill_value == b.fill_value``, return the fill value,
    otherwise return None.

    Parameters
    ----------
    a, b : MaskedArray
        The masked arrays for which to compare fill values.

    Returns
    -------
    fill_value : scalar or None
        The common fill value, or None.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.ma.array([0, 1.], fill_value=3)
    >>> y = np.ma.array([0, 1.], fill_value=3)
    >>> np.ma.common_fill_value(x, y)
    3.0

    """
    t1 = get_fill_value(a)
    t2 = get_fill_value(b)
    if t1 == t2:
        return t1
    return None

