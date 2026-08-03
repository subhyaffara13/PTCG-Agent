import copy

def masked_less_equal(x, value, copy=True):
    """
    Mask an array where less than or equal to a given value.

    This function is a shortcut to ``masked_where``, with
    `condition` = (x <= value).

    See Also
    --------
    masked_where : Mask where a condition is met.

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> a = np.arange(4)
    >>> a
    array([0, 1, 2, 3])
    >>> ma.masked_less_equal(a, 2)
    masked_array(data=[--, --, --, 3],
                 mask=[ True,  True,  True, False],
           fill_value=999999)

    """
    return masked_where(less_equal(x, value), x, copy=copy)

