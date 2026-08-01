
def nanmax(a, axis=None, out=None, keepdims=np._NoValue, initial=np._NoValue,
           where=np._NoValue):
    """
    Return the maximum of an array or maximum along an axis, ignoring any
    NaNs.  When all-NaN slices are encountered a ``RuntimeWarning`` is
    raised and NaN is returned for that slice.

    Parameters
    ----------
    a : array_like
        Array containing numbers whose maximum is desired. If `a` is not an
        array, a conversion is attempted.
    axis : {int, tuple of int, None}, optional
        Axis or axes along which the maximum is computed. The default is to compute
        the maximum of the flattened array.
    out : ndarray, optional
        Alternate output array in which to place the result.  The default
        is ``None``; if provided, it must have the same shape as the
        expected output, but the type will be cast if necessary. See
        :ref:`ufuncs-output-type` for more details.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the original `a`.
        If the value is anything but the default, then
        `keepdims` will be passed through to the `max` method
        of sub-classes of `ndarray`.  If the sub-classes methods
        does not implement `keepdims` any exceptions will be raised.
    initial : scalar, optional
        The minimum value of an output element. Must be present to allow
        computation on empty slice. See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.22.0
    where : array_like of bool, optional
        Elements to compare for the maximum. See `~numpy.ufunc.reduce`
        for details.

        .. versionadded:: 1.22.0

    Returns
    -------
    nanmax : ndarray
        An array with the same shape as `a`, with the specified axis removed.
        If `a` is a 0-d array, or if axis is None, an ndarray scalar is
        returned.  The same dtype as `a` is returned.

    See Also
    --------
    nanmin :
        The minimum value of an array along a given axis, ignoring any NaNs.
    amax :
        The maximum value of an array along a given axis, propagating any NaNs.
    fmax :
        Element-wise maximum of two arrays, ignoring any NaNs.
    maximum :
        Element-wise maximum of two arrays, propagating any NaNs.
    isnan :
        Shows which elements are Not a Number (NaN).
    isfinite:
        Shows which elements are neither NaN nor infinity.

    amin, fmin, minimum

    Notes
    -----
    NumPy uses the IEEE Standard for Binary Floating-Point for Arithmetic
    (IEEE 754). This means that Not a Number is not equivalent to infinity.
    Positive infinity is treated as a very large number and negative
    infinity is treated as a very small (i.e. negative) number.

    If the input has a integer type the function is equivalent to np.max.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2], [3, np.nan]])
    >>> np.nanmax(a)
    3.0
    >>> np.nanmax(a, axis=0)
    array([3.,  2.])
    >>> np.nanmax(a, axis=1)
    array([2.,  3.])

    When positive infinity and negative infinity are present:

    >>> np.nanmax([1, 2, np.nan, -np.inf])
    2.0
    >>> np.nanmax([1, 2, np.nan, np.inf])
    inf

    """
    kwargs = {}
    if keepdims is not np._NoValue:
        kwargs['keepdims'] = keepdims
    if initial is not np._NoValue:
        kwargs['initial'] = initial
    if where is not np._NoValue:
        kwargs['where'] = where

    if (type(a) is np.ndarray or type(a) is np.memmap) and a.dtype != np.object_:
        # Fast, but not safe for subclasses of ndarray, or object arrays,
        # which do not implement isnan (gh-9009), or fmax correctly (gh-8975)
        res = np.fmax.reduce(a, axis=axis, out=out, **kwargs)
        if np.isnan(res).any():
            warnings.warn("All-NaN slice encountered", RuntimeWarning,
                          stacklevel=2)
    else:
        # Slow, but safe for subclasses of ndarray
        a, mask = _replace_nan(a, -np.inf)
        res = np.amax(a, axis=axis, out=out, **kwargs)
        if mask is None:
            return res

        # Check for all-NaN axis
        kwargs.pop("initial", None)
        mask = np.all(mask, axis=axis, **kwargs)
        if np.any(mask):
            res = _copyto(res, np.nan, mask)
            warnings.warn("All-NaN axis encountered", RuntimeWarning,
                          stacklevel=2)
    return res


def nanmax(a: ArrayLike, axis: Axis = None, out: None = None,
           keepdims: bool = False, initial: ArrayLike | None = None,
           where: ArrayLike | None = None) -> Array:
  r"""Return the maximum of the array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanmax`.

  Args:
    a: Input array.
    axis: int or sequence of ints, default=None. Axis along which the maximum is
      computed. If None, the maximum is computed along the flattened array.
    keepdims: bool, default=False. If True, reduced axes are left in the result
      with size 1.
    initial: int or array, default=None. Initial value for the maximum.
    where: array of boolean dtype, default=None. The elements to be used in the
      maximum. Array should be broadcast compatible to the input. ``initial``
      must be specified when ``where`` is used.
    out: Unused by JAX.

  Returns:
    An array of maximum values along the given axis, ignoring NaNs. If all values
    are NaNs along the given axis, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmin`: Compute the minimum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nansum`: Compute the sum of array elements along a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanprod`: Compute the product of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements along a given
      axis, ignoring NaNs.

  Examples:

    By default, ``jnp.nanmax`` computes the maximum of elements along the flattened
    array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[8, nan, 4, 6],
    ...                [nan, -2, nan, -4],
    ...                [-2, 1, 7, nan]])
    >>> jnp.nanmax(x)
    Array(8., dtype=float32)

    If ``axis=1``, the maximum will be computed along axis 1.

    >>> jnp.nanmax(x, axis=1)
    Array([ 8., -2.,  7.], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.nanmax(x, axis=1, keepdims=True)
    Array([[ 8.],
           [-2.],
           [ 7.]], dtype=float32)

    To include only specific elements in computing the maximum, you can use
    ``where``. It can either have same dimension as input

    >>> where=jnp.array([[0, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.nanmax(x, axis=1, keepdims=True, initial=0, where=where)
    Array([[4.],
           [0.],
           [7.]], dtype=float32)

    or must be broadcast compatible with input.

    >>> where = jnp.array([[True],
    ...                    [False],
    ...                    [False]])
    >>> jnp.nanmax(x, axis=0, keepdims=True, initial=0, where=where)
    Array([[8., 0., 4., 6.]], dtype=float32)
  """
  return _nan_reduction(a, 'nanmax', max, -np.inf, nan_if_all_nan=initial is None,
                        axis=axis, out=out, keepdims=keepdims,
                        initial=initial, where=where)

