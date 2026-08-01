
def nansum(self, dim=None, keepdim=False, *, dtype=None):
    return aten.sum(torch.where(torch.isnan(self), 0, self), dim, keepdim, dtype=dtype)


def nansum(
    values: np.ndarray,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    min_count: int = 0,
    mask: npt.NDArray[np.bool_] | None = None,
) -> npt.NDArray[np.floating] | float | NaTType:
    """
    Sum the elements along an axis ignoring NaNs

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
    result : dtype

    Examples
    --------
    >>> from pandas.core import nanops
    >>> s = pd.Series([1, 2, np.nan])
    >>> nanops.nansum(s.values)
    np.float64(3.0)
    """
    dtype = values.dtype
    values, mask = _get_values(values, skipna, fill_value=0, mask=mask)
    dtype_sum = _get_dtype_max(dtype)
    if dtype.kind == "f":
        dtype_sum = dtype
    elif dtype.kind == "m":
        dtype_sum = np.dtype(np.float64)

    the_sum = values.sum(axis, dtype=dtype_sum)
    the_sum = _maybe_null_out(the_sum, axis, mask, values.shape, min_count=min_count)

    return the_sum


def nansum(a, axis=None, dtype=None, out=None, keepdims=np._NoValue,
           initial=np._NoValue, where=np._NoValue):
    """
    Return the sum of array elements over a given axis treating Not a
    Numbers (NaNs) as zero.

    In NumPy versions <= 1.9.0 Nan is returned for slices that are all-NaN or
    empty. In later versions zero is returned.

    Parameters
    ----------
    a : array_like
        Array containing numbers whose sum is desired. If `a` is not an
        array, a conversion is attempted.
    axis : {int, tuple of int, None}, optional
        Axis or axes along which the sum is computed. The default is to compute the
        sum of the flattened array.
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
        expected output, but the type will be cast if necessary.  See
        :ref:`ufuncs-output-type` for more details. The casting of NaN to integer
        can yield unexpected results.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the original `a`.

        If the value is anything but the default, then
        `keepdims` will be passed through to the `mean` or `sum` methods
        of sub-classes of `ndarray`.  If the sub-classes methods
        does not implement `keepdims` any exceptions will be raised.
    initial : scalar, optional
        Starting value for the sum. See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.22.0
    where : array_like of bool, optional
        Elements to include in the sum. See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.22.0

    Returns
    -------
    nansum : ndarray.
        A new array holding the result is returned unless `out` is
        specified, in which it is returned. The result has the same
        size as `a`, and the same shape as `a` if `axis` is not None
        or `a` is a 1-d array.

    See Also
    --------
    numpy.sum : Sum across array propagating NaNs.
    isnan : Show which elements are NaN.
    isfinite : Show which elements are not NaN or +/-inf.

    Notes
    -----
    If both positive and negative infinity are present, the sum will be Not
    A Number (NaN).

    Examples
    --------
    >>> import numpy as np
    >>> np.nansum(1)
    1
    >>> np.nansum([1])
    1
    >>> np.nansum([1, np.nan])
    1.0
    >>> a = np.array([[1, 1], [1, np.nan]])
    >>> np.nansum(a)
    3.0
    >>> np.nansum(a, axis=0)
    array([2.,  1.])
    >>> np.nansum([1, np.nan, np.inf])
    inf
    >>> np.nansum([1, np.nan, -np.inf])
    -inf
    >>> with np.errstate(invalid="ignore"):
    ...     np.nansum([1, np.nan, np.inf, -np.inf]) # both +/- infinity present
    np.float64(nan)

    """
    a, mask = _replace_nan(a, 0)
    return np.sum(a, axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                  initial=initial, where=where)


def nansum(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
           out: None = None,
           keepdims: bool = False, initial: ArrayLike | None = None,
           where: ArrayLike | None = None) -> Array:
  r"""Return the sum of the array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nansum`.

  Args:
    a: Input array.
    axis: int or sequence of ints, default=None. Axis along which the sum is
      computed. If None, the sum is computed along the flattened array.
    dtype: The type of the output array. Default=None.
    keepdims: bool, default=False. If True, reduced axes are left in the result
      with size 1.
    initial: int or array, default=None. Initial value for the sum.
    where: array of boolean dtype, default=None. The elements to be used in the
      sum. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array containing the sum of array elements along the given axis, ignoring
    NaNs. If all elements along the given axis are NaNs, returns 0.

  See also:
    - :func:`jax.numpy.nanmin`: Compute the minimum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmax`: Compute the maximum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanprod`: Compute the product of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements along a given
      axis, ignoring NaNs.

  Examples:

    By default, ``jnp.nansum`` computes the sum of elements along the flattened
    array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[3, nan, 4, 5],
    ...                [nan, -2, nan, 7],
    ...                [2, 1, 6, nan]])
    >>> jnp.nansum(x)
    Array(26., dtype=float32)

    If ``axis=1``, the sum will be computed along axis 1.

    >>> jnp.nansum(x, axis=1)
    Array([12.,  5.,  9.], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.nansum(x, axis=1, keepdims=True)
    Array([[12.],
           [ 5.],
           [ 9.]], dtype=float32)

    To include only specific elements in computing the sum, you can use ``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.nansum(x, axis=1, keepdims=True, where=where)
    Array([[7.],
           [7.],
           [9.]], dtype=float32)

    If ``where`` is ``False`` at all elements, ``jnp.nansum`` returns 0 along
    the given axis.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.nansum(x, axis=0, keepdims=True, where=where)
    Array([[0., 0., 0., 0.]], dtype=float32)
  """
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "nanprod")
  return _nan_reduction(a, 'nansum', sum, 0, nan_if_all_nan=False,
                        axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                        initial=initial, where=where)

