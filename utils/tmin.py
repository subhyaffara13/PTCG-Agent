
def tmin(a, lowerlimit=None, axis=0, inclusive=True):
    """
    Compute the trimmed minimum

    Parameters
    ----------
    a : array_like
        array of values
    lowerlimit : None or float, optional
        Values in the input array less than the given limit will be ignored.
        When lowerlimit is None, then all values are used. The default value
        is None.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over the
        whole array `a`.
    inclusive : {True, False}, optional
        This flag determines whether values exactly equal to the lower limit
        are included.  The default value is True.

    Returns
    -------
    tmin : float, int or ndarray

    Notes
    -----
    For more details on `tmin`, see `scipy.stats.tmin`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import mstats
    >>> a = np.array([[6, 8, 3, 0],
    ...               [3, 2, 1, 2],
    ...               [8, 1, 8, 2],
    ...               [5, 3, 0, 2],
    ...               [4, 7, 5, 2]])
    ...
    >>> mstats.tmin(a, 5)
    masked_array(data=[5, 7, 5, --],
                 mask=[False, False, False,  True],
           fill_value=999999)

    """  # numpydoc ignore=RT03
    a, axis = _chk_asarray(a, axis)
    am = trima(a, (lowerlimit, None), (inclusive, False))
    return ma.minimum.reduce(am, axis)


def tmin(a, lowerlimit=None, axis=0, inclusive=True, nan_policy='propagate'):
    """Compute the trimmed minimum.

    This function finds the minimum value of an array `a` along the
    specified axis, but only considering values greater than a specified
    lower limit.

    Parameters
    ----------
    a : array_like
        Array of values.
    lowerlimit : None or float, optional
        Values in the input array less than the given limit will be ignored.
        When lowerlimit is None, then all values are used. The default value
        is None.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over the
        whole array `a`.
    inclusive : {True, False}, optional
        This flag determines whether values exactly equal to the lower limit
        are included.  The default value is True.

    Returns
    -------
    tmin : float, int or ndarray
        Trimmed minimum.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.tmin(x)
    0

    >>> stats.tmin(x, 13)
    13

    >>> stats.tmin(x, 13, inclusive=False)
    14

    """
    xp = array_namespace(a)

    max_ = xp.iinfo(a.dtype).max if xp.isdtype(a.dtype, 'integral') else xp.inf
    a, mask = _put_val_to_limits(a, (lowerlimit, None), (inclusive, None),
                                 val=max_, xp=xp)

    res = xp.min(a, axis=axis)
    invalid = xp.all(mask, axis=axis)  # All elements are below lowerlimit

    # For eager backends, output dtype is data-dependent
    if is_lazy_array(invalid) or xp.any(invalid):
        # Possible loss of precision for int types
        res = xp_promote(res, force_floating=True, xp=xp)
        res = xp.where(invalid, xp.nan, res)

    return res[()] if res.ndim == 0 else res

