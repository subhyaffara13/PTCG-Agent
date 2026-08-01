
def _pow(mul_f, c, pow, maxpower):
    """
    Helper function used to implement the ``<type>pow`` functions.

    Parameters
    ----------
    mul_f : function(array_like, array_like) -> ndarray
        The ``<type>mul`` function, such as ``polymul``
    c : array_like
        1-D array of array of series coefficients
    pow, maxpower
        See the ``<type>pow`` functions for more detail
    """
    # c is a trimmed copy
    [c] = as_series([c])
    power = int(pow)
    if power != pow or power < 0:
        raise ValueError("Power must be a non-negative integer.")
    elif maxpower is not None and power > maxpower:
        raise ValueError("Power is too large")
    elif power == 0:
        return np.array([1], dtype=c.dtype)
    elif power == 1:
        return c
    else:
        # This can be made more efficient by using powers of two
        # in the usual way.
        prd = c
        for i in range(2, power + 1):
            prd = mul_f(prd, c)
        return prd

