
def tmax(a, upperlimit=None, axis=0, inclusive=True):
    """
    Compute the trimmed maximum

    This function computes the maximum value of an array along a given axis,
    while ignoring values larger than a specified upper limit.

    Parameters
    ----------
    a : array_like
        array of values
    upperlimit : None or float, optional
        Values in the input array greater than the given limit will be ignored.
        When upperlimit is None, then all values are used. The default value
        is None.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over the
        whole array `a`.
    inclusive : {True, False}, optional
        This flag determines whether values exactly equal to the upper limit
        are included.  The default value is True.

    Returns
    -------
    tmax : float, int or ndarray

    Notes
    -----
    For more details on `tmax`, see `scipy.stats.tmax`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import mstats
    >>> a = np.array([[6, 8, 3, 0],
    ...               [3, 9, 1, 2],
    ...               [8, 7, 8, 2],
    ...               [5, 6, 0, 2],
    ...               [4, 5, 5, 2]])
    ...
    ...
    >>> mstats.tmax(a, 4)
    masked_array(data=[4, --, 3, 2],
                 mask=[False,  True, False, False],
           fill_value=999999)

    """  # numpydoc ignore=RT03
    a, axis = _chk_asarray(a, axis)
    am = trima(a, (None, upperlimit), (False, inclusive))
    return ma.maximum.reduce(am, axis)


def tmax(a, upperlimit=None, axis=0, inclusive=True, nan_policy='propagate'):
    """Compute the trimmed maximum.

    This function computes the maximum value of an array along a given axis,
    while ignoring values larger than a specified upper limit.

    Parameters
    ----------
    a : array_like
        Array of values.
    upperlimit : None or float, optional
        Values in the input array greater than the given limit will be ignored.
        When upperlimit is None, then all values are used. The default value
        is None.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over the
        whole array `a`.
    inclusive : {True, False}, optional
        This flag determines whether values exactly equal to the upper limit
        are included.  The default value is True.

    Returns
    -------
    tmax : float, int or ndarray
        Trimmed maximum.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.tmax(x)
    19

    >>> stats.tmax(x, 13)
    13

    >>> stats.tmax(x, 13, inclusive=False)
    12

    """
    xp = array_namespace(a)

    min_ = xp.iinfo(a.dtype).min if xp.isdtype(a.dtype, 'integral') else -xp.inf
    a, mask = _put_val_to_limits(a, (None, upperlimit), (None, inclusive),
                                 val=min_, xp=xp)

    res = xp.max(a, axis=axis)
    invalid = xp.all(mask, axis=axis)  # All elements are above upperlimit

    # For eager backends, output dtype is data-dependent
    if is_lazy_array(invalid) or xp.any(invalid):
        # Possible loss of precision for int types
        res = xp_promote(res, force_floating=True, xp=xp)
        res = xp.where(invalid, xp.nan, res)

    return res[()] if res.ndim == 0 else res

