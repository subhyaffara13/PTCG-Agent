import copy

def fix_invalid(a, mask=nomask, copy=True, fill_value=None):
    """
    Return input with invalid data masked and replaced by a fill value.

    Invalid data means values of `nan`, `inf`, etc.

    Parameters
    ----------
    a : array_like
        Input array, a (subclass of) ndarray.
    mask : sequence, optional
        Mask. Must be convertible to an array of booleans with the same
        shape as `data`. True indicates a masked (i.e. invalid) data.
    copy : bool, optional
        Whether to use a copy of `a` (True) or to fix `a` in place (False).
        Default is True.
    fill_value : scalar, optional
        Value used for fixing invalid data. Default is None, in which case
        the ``a.fill_value`` is used.

    Returns
    -------
    b : MaskedArray
        The input array with invalid entries fixed.

    Notes
    -----
    A copy is performed by default.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.ma.array([1., -1, np.nan, np.inf], mask=[1] + [0]*3)
    >>> x
    masked_array(data=[--, -1.0, nan, inf],
                 mask=[ True, False, False, False],
           fill_value=1e+20)
    >>> np.ma.fix_invalid(x)
    masked_array(data=[--, -1.0, --, --],
                 mask=[ True, False,  True,  True],
           fill_value=1e+20)

    >>> fixed = np.ma.fix_invalid(x)
    >>> fixed.data
    array([ 1.e+00, -1.e+00,  1.e+20,  1.e+20])
    >>> x.data
    array([ 1., -1., nan, inf])

    """
    a = masked_array(a, copy=copy, mask=mask, subok=True)
    invalid = np.logical_not(np.isfinite(a._data))
    if not invalid.any():
        return a
    a._mask |= invalid
    if fill_value is None:
        fill_value = a.fill_value
    a._data[invalid] = fill_value
    return a

