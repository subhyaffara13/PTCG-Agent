
def masked_equal(x, value, copy=True):
    """
    Mask an array where equal to a given value.

    Return a MaskedArray, masked where the data in array `x` are
    equal to `value`. The fill_value of the returned MaskedArray
    is set to `value`.

    For floating point arrays, consider using ``masked_values(x, value)``.

    See Also
    --------
    masked_where : Mask where a condition is met.
    masked_values : Mask using floating point equality.

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> a = np.arange(4)
    >>> a
    array([0, 1, 2, 3])
    >>> ma.masked_equal(a, 2)
    masked_array(data=[0, 1, --, 3],
                 mask=[False, False,  True, False],
           fill_value=2)

    """
    output = masked_where(equal(x, value), x, copy=copy)
    output.fill_value = value
    return output

