
def asarray_chkfinite(a, dtype=None, order=None):
    """Convert the input to an array, checking for NaNs or Infs.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.  This
        includes lists, lists of tuples, tuples, tuples of tuples, tuples
        of lists and ndarrays.  Success requires no NaNs or Infs.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F', 'A', 'K'}, optional
        The memory layout of the output.
        'C' gives a row-major layout (C-style),
        'F' gives a column-major layout (Fortran-style).
        'C' and 'F' will copy if needed to ensure the output format.
        'A' (any) is equivalent to 'F' if input a is non-contiguous or
        Fortran-contiguous, otherwise, it is equivalent to 'C'.
        Unlike 'C' or 'F', 'A' does not ensure that the result is contiguous.
        'K' (keep) preserves the input order for the output.
        'C' is the default.

    Returns
    -------
    out : ndarray
        Array interpretation of `a`.  No copy is performed if the input
        is already an ndarray.  If `a` is a subclass of ndarray, a base
        class ndarray is returned.

    Raises
    ------
    ValueError
        Raises ValueError if `a` contains NaN (Not a Number) or Inf (Infinity).

    See Also
    --------
    asarray : Create and array.
    asanyarray : Similar function which passes through subclasses.
    ascontiguousarray : Convert input to a contiguous array.
    asfortranarray : Convert input to an ndarray with column-major
                     memory order.
    fromiter : Create an array from an iterator.
    fromfunction : Construct an array by executing a function on grid
                   positions.

    Examples
    --------
    >>> import numpy as np

    Convert a list into an array. If all elements are finite, then
    ``asarray_chkfinite`` is identical to ``asarray``.

    >>> a = [1, 2]
    >>> np.asarray_chkfinite(a, dtype=np.float64)
    array([1., 2.])

    Raises ValueError if array_like contains Nans or Infs.

    >>> a = [1, 2, np.inf]
    >>> try:
    ...     np.asarray_chkfinite(a)
    ... except ValueError:
    ...     print('ValueError')
    ...
    ValueError

    """
    a = asarray(a, dtype=dtype, order=order)
    if a.dtype.char in typecodes['AllFloat'] and not np.isfinite(a).all():
        raise ValueError(
            "array must not contain infs or NaNs")
    return a

