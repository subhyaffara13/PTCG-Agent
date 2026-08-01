
def nanprod(
    values: np.ndarray,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    min_count: int = 0,
    mask: npt.NDArray[np.bool_] | None = None,
) -> float:
    """
    Parameters
    ----------
    values : ndarray[dtype]
    axis : int, optional
    skipna : bool, default True
    min_count: int, default 0
    mask : ndarray[bool], optional
        nan-mask if known

    Returns
    -------
    Dtype
        The product of all elements on a given axis. ( NaNs are treated as 1)

    Examples
    --------
    >>> from pandas.core import nanops
    >>> s = pd.Series([1, 2, 3, np.nan])
    >>> nanops.nanprod(s.values)
    np.float64(6.0)
    """
    mask = _maybe_get_mask(values, skipna, mask)

    if skipna and mask is not None:
        values = values.copy()
        values[mask] = 1
    result = values.prod(axis)
    # error: Incompatible return value type (got "Union[ndarray, float]", expected
    # "float")
    return _maybe_null_out(  # type: ignore[return-value]
        result, axis, mask, values.shape, min_count=min_count
    )


def nanprod(a, axis=None, dtype=None, out=None, keepdims=np._NoValue,
            initial=np._NoValue, where=np._NoValue):
    """
    Return the product of array elements over a given axis treating Not a
    Numbers (NaNs) as ones.

    One is returned for slices that are all-NaN or empty.

    Parameters
    ----------
    a : array_like
        Array containing numbers whose product is desired. If `a` is not an
        array, a conversion is attempted.
    axis : {int, tuple of int, None}, optional
        Axis or axes along which the product is computed. The default is to compute
        the product of the flattened array.
    dtype : data-type, optional
        The type of the returned array and of the accumulator in which the
        elements are summed.  By default, the dtype of `a` is used.  An
        exception is when `a` has an integer type with less precision than
        the platform (u)intp. In that case, the default will be either
        (u)int32 or (u)int64 depending on whether the platform is 32 or 64
        bits. For inexact inputs, dtype must be inexact.
    out : ndarray, optional
        Alternate output array in which to place the result.  The default
        is ``None``. If provided, it must have the same shape as the
        expected output, but the type will be cast if necessary. See
        :ref:`ufuncs-output-type` for more details. The casting of NaN to integer
        can yield unexpected results.
    keepdims : bool, optional
        If True, the axes which are reduced are left in the result as
        dimensions with size one. With this option, the result will
        broadcast correctly against the original `arr`.
    initial : scalar, optional
        The starting value for this product. See `~numpy.ufunc.reduce`
        for details.

        .. versionadded:: 1.22.0
    where : array_like of bool, optional
        Elements to include in the product. See `~numpy.ufunc.reduce`
        for details.

        .. versionadded:: 1.22.0

    Returns
    -------
    nanprod : ndarray
        A new array holding the result is returned unless `out` is
        specified, in which case it is returned.

    See Also
    --------
    numpy.prod : Product across array propagating NaNs.
    isnan : Show which elements are NaN.

    Examples
    --------
    >>> import numpy as np
    >>> np.nanprod(1)
    1
    >>> np.nanprod([1])
    1
    >>> np.nanprod([1, np.nan])
    1.0
    >>> a = np.array([[1, 2], [3, np.nan]])
    >>> np.nanprod(a)
    6.0
    >>> np.nanprod(a, axis=0)
    array([3., 2.])

    """
    a, mask = _replace_nan(a, 1)
    return np.prod(a, axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                   initial=initial, where=where)


def nanprod(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
            keepdims: bool = False, initial: ArrayLike | None = None,
            where: ArrayLike | None = None) -> Array:
  r"""Return the product of the array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanprod`.

  Args:
    a: Input array.
    axis: int or sequence of ints, default=None. Axis along which the product is
      computed. If None, the product is computed along the flattened array.
    dtype: The type of the output array. Default=None.
    keepdims: bool, default=False. If True, reduced axes are left in the result
      with size 1.
    initial: int or array, default=None. Initial value for the product.
    where: array of boolean dtype, default=None. The elements to be used in the
      product. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array containing the product of array elements along the given axis,
    ignoring NaNs. If all elements along the given axis are NaNs, returns 1.

  See also:
    - :func:`jax.numpy.nanmin`: Compute the minimum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmax`: Compute the maximum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nansum`: Compute the sum of array elements along a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements along a given
      axis, ignoring NaNs.

  Examples:

    By default, ``jnp.nanprod`` computes the product of elements along the flattened
    array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[nan, 3, 4, nan],
    ...                [5, nan, 1, 3],
    ...                [2, 1, nan, 1]])
    >>> jnp.nanprod(x)
    Array(360., dtype=float32)

    If ``axis=1``, the product will be computed along axis 1.

    >>> jnp.nanprod(x, axis=1)
    Array([12., 15.,  2.], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.nanprod(x, axis=1, keepdims=True)
    Array([[12.],
           [15.],
           [ 2.]], dtype=float32)

    To include only specific elements in computing the maximum, you can use ``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.nanprod(x, axis=1, keepdims=True, where=where)
    Array([[4.],
           [3.],
           [2.]], dtype=float32)

    If ``where`` is ``False`` at all elements, ``jnp.nanprod`` returns 1 along
    the given axis.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.nanprod(x, axis=0, keepdims=True, where=where)
    Array([[1., 1., 1., 1.]], dtype=float32)
  """
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "nanprod")
  return _nan_reduction(a, 'nanprod', prod, 1, nan_if_all_nan=False,
                        axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                        initial=initial, where=where)

