import copy

def masked_values(x, value, rtol=1e-5, atol=1e-8, copy=True, shrink=True):
    """
    Mask using floating point equality.

    Return a MaskedArray, masked where the data in array `x` are approximately
    equal to `value`, determined using `isclose`. The default tolerances for
    `masked_values` are the same as those for `isclose`.

    For integer types, exact equality is used, in the same way as
    `masked_equal`.

    The fill_value is set to `value` and the mask is set to ``nomask`` if
    possible.

    Parameters
    ----------
    x : array_like
        Array to mask.
    value : float
        Masking value.
    rtol, atol : float, optional
        Tolerance parameters passed on to `isclose`
    copy : bool, optional
        Whether to return a copy of `x`.
    shrink : bool, optional
        Whether to collapse a mask full of False to ``nomask``.

    Returns
    -------
    result : MaskedArray
        The result of masking `x` where approximately equal to `value`.

    See Also
    --------
    masked_where : Mask where a condition is met.
    masked_equal : Mask where equal to a given value (integers).

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> x = np.array([1, 1.1, 2, 1.1, 3])
    >>> ma.masked_values(x, 1.1)
    masked_array(data=[1.0, --, 2.0, --, 3.0],
                 mask=[False,  True, False,  True, False],
           fill_value=1.1)

    Note that `mask` is set to ``nomask`` if possible.

    >>> ma.masked_values(x, 2.1)
    masked_array(data=[1. , 1.1, 2. , 1.1, 3. ],
                 mask=False,
           fill_value=2.1)

    Unlike `masked_equal`, `masked_values` can perform approximate equalities.

    >>> ma.masked_values(x, 2.1, atol=1e-1)
    masked_array(data=[1.0, 1.1, --, 1.1, 3.0],
                 mask=[False, False,  True, False, False],
           fill_value=2.1)

    """
    xnew = filled(x, value)
    if np.issubdtype(xnew.dtype, np.floating):
        mask = np.isclose(xnew, value, atol=atol, rtol=rtol)
    else:
        mask = umath.equal(xnew, value)
    ret = masked_array(xnew, mask=mask, copy=copy, fill_value=value)
    if shrink:
        ret.shrink_mask()
    return ret

