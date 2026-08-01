
def allequal(a, b, fill_value=True):
    """
    Return True if all entries of a and b are equal, using
    fill_value as a truth value where either or both are masked.

    Parameters
    ----------
    a, b : array_like
        Input arrays to compare.
    fill_value : bool, optional
        Whether masked values in a or b are considered equal (True) or not
        (False).

    Returns
    -------
    y : bool
        Returns True if the two arrays are equal within the given
        tolerance, False otherwise. If either array contains NaN,
        then False is returned.

    See Also
    --------
    all, any
    numpy.ma.allclose

    Examples
    --------
    >>> import numpy as np
    >>> a = np.ma.array([1e10, 1e-7, 42.0], mask=[0, 0, 1])
    >>> a
    masked_array(data=[10000000000.0, 1e-07, --],
                 mask=[False, False,  True],
           fill_value=1e+20)

    >>> b = np.array([1e10, 1e-7, -42.0])
    >>> b
    array([  1.00000000e+10,   1.00000000e-07,  -4.20000000e+01])
    >>> np.ma.allequal(a, b, fill_value=False)
    False
    >>> np.ma.allequal(a, b)
    True

    """
    m = mask_or(getmask(a), getmask(b))
    if m is nomask:
        x = getdata(a)
        y = getdata(b)
        d = umath.equal(x, y)
        return d.all()
    elif fill_value:
        x = getdata(a)
        y = getdata(b)
        d = umath.equal(x, y)
        dm = array(d, mask=m, copy=False)
        return dm.filled(True).all(None)
    else:
        return False

