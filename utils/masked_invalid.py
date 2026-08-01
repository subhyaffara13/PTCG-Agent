
def masked_invalid(a, copy=True):
    """
    Mask an array where invalid values occur (NaNs or infs).

    This function is a shortcut to ``masked_where``, with
    `condition` = ~(np.isfinite(a)). Any pre-existing mask is conserved.
    Only applies to arrays with a dtype where NaNs or infs make sense
    (i.e. floating point types), but accepts any array_like object.

    See Also
    --------
    masked_where : Mask where a condition is met.

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> a = np.arange(5, dtype=np.float64)
    >>> a[2] = np.nan
    >>> a[3] = np.inf
    >>> a
    array([ 0.,  1., nan, inf,  4.])
    >>> ma.masked_invalid(a)
    masked_array(data=[0.0, 1.0, --, --, 4.0],
                 mask=[False, False,  True,  True, False],
           fill_value=1e+20)

    """
    a = np.array(a, copy=None, subok=True)
    res = masked_where(~(np.isfinite(a)), a, copy=copy)
    # masked_invalid previously never returned nomask as a mask and doing so
    # threw off matplotlib (gh-22842).  So use shrink=False:
    if res._mask is nomask:
        res._mask = make_mask_none(res.shape, res.dtype)
    return res

