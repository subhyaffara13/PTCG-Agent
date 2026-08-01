
def fix(x, out=None):
    """
    Round to nearest integer towards zero.

    .. deprecated:: 2.5
        `numpy.fix` is deprecated. Use `numpy.trunc` instead,
        which is faster and follows the Array API standard.

    Round an array of floats element-wise to nearest integer towards zero.
    The rounded values have the same data-type as the input.

    Parameters
    ----------
    x : array_like
        An array to be rounded
    out : ndarray, optional
        A location into which the result is stored. If provided, it must have
        a shape that the input broadcasts to. If not provided or None, a
        freshly-allocated array is returned.

    Returns
    -------
    out : ndarray of floats
        An array with the same dimensions and data-type as the input.
        If second argument is not supplied then a new array is returned
        with the rounded values.

        If a second argument is supplied the result is stored there.
        The return value ``out`` is then a reference to that array.

    See Also
    --------
    rint, trunc, floor, ceil
    around : Round to given number of decimals

    Examples
    --------
    >>> import numpy as np
    >>> np.fix(3.14)
    3.0
    >>> np.fix(3)
    3
    >>> np.fix([2.1, 2.9, -2.1, -2.9])
    array([ 2.,  2., -2., -2.])

    """
    # Deprecated in NumPy 2.5, 2026-01-12
    warnings.warn(
        "numpy.fix is deprecated. Use numpy.trunc instead, "
        "which is faster and follows the Array API standard.",
        DeprecationWarning,
        stacklevel=2,
    )
    return nx.trunc(x, out=out)

