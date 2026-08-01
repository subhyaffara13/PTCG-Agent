
def round_(a, decimals=0, out=None):
    """
    Return a copy of a, rounded to 'decimals' places.

    .. deprecated:: 2.5
        `numpy.ma.round_` is deprecated. Use `numpy.ma.round` instead.

    When 'decimals' is negative, it specifies the number of positions
    to the left of the decimal point.  The real and imaginary parts of
    complex numbers are rounded separately. Nothing is done if the
    array is not of float type and 'decimals' is greater than or equal
    to 0.

    Parameters
    ----------
    decimals : int
        Number of decimals to round to. May be negative.
    out : array_like
        Existing array to use for output.
        If not given, returns a default copy of a.

    Notes
    -----
    If out is given and does not have a mask attribute, the mask of a
    is lost!

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> x = [11.2, -3.973, 0.801, -1.41]
    >>> mask = [0, 0, 0, 1]
    >>> masked_x = ma.masked_array(x, mask)
    >>> masked_x
    masked_array(data=[11.2, -3.973, 0.801, --],
                 mask=[False, False, False, True],
        fill_value=1e+20)
    >>> ma.round_(masked_x)
    masked_array(data=[11.0, -4.0, 1.0, --],
                 mask=[False, False, False, True],
        fill_value=1e+20)
    >>> ma.round(masked_x, decimals=1)
    masked_array(data=[11.2, -4.0, 0.8, --],
                 mask=[False, False, False, True],
        fill_value=1e+20)
    >>> ma.round_(masked_x, decimals=-1)
    masked_array(data=[10.0, -0.0, 0.0, --],
                 mask=[False, False, False, True],
        fill_value=1e+20)
    """
    warnings.warn(
        "numpy.ma.round_ is deprecated. Use numpy.ma.round instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return round(a, decimals, out)

