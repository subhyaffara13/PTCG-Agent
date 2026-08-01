
def nanmean(
    values: np.ndarray,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    mask: npt.NDArray[np.bool_] | None = None,
) -> float:
    """
    Compute the mean of the element along an axis ignoring NaNs

    Parameters
    ----------
    values : ndarray
    axis : int, optional
    skipna : bool, default True
    mask : ndarray[bool], optional
        nan-mask if known

    Returns
    -------
    float
        Unless input is a float array, in which case use the same
        precision as the input array.

    Examples
    --------
    >>> from pandas.core import nanops
    >>> s = pd.Series([1, 2, np.nan])
    >>> nanops.nanmean(s.values)
    np.float64(1.5)
    """
    if values.dtype == object and len(values) > 1_000 and mask is None:
        # GH#54754 if we are going to fail, try to fail-fast
        nanmean(values[:1000], axis=axis, skipna=skipna)

    dtype = values.dtype
    values, mask = _get_values(values, skipna, fill_value=0, mask=mask)
    dtype_sum = _get_dtype_max(dtype)
    dtype_count = np.dtype(np.float64)

    # not using needs_i8_conversion because that includes period
    if dtype.kind in "mM":
        dtype_sum = np.dtype(np.float64)
    elif dtype.kind in "iu":
        dtype_sum = np.dtype(np.float64)
    elif dtype.kind == "f":
        dtype_sum = dtype
        dtype_count = dtype

    count = _get_counts(values.shape, mask, axis, dtype=dtype_count)
    the_sum = values.sum(axis, dtype=dtype_sum)
    the_sum = _ensure_numeric(the_sum)

    if axis is not None and getattr(the_sum, "ndim", False):
        count = cast(np.ndarray, count)
        with np.errstate(all="ignore"):
            # suppress division by zero warnings
            the_mean = the_sum / count
        ct_mask = count == 0
        if ct_mask.any():
            the_mean[ct_mask] = np.nan
    else:
        the_mean = the_sum / count if count > 0 else np.nan

    return the_mean


def nanmean(a, axis=None, dtype=None, out=None, keepdims=np._NoValue,
            *, where=np._NoValue):
    """
    Compute the arithmetic mean along the specified axis, ignoring NaNs.

    Returns the average of the array elements.  The average is taken over
    the flattened array by default, otherwise over the specified axis.
    `float64` intermediate and return values are used for integer inputs.

    For all-NaN slices, NaN is returned and a `RuntimeWarning` is raised.

    Parameters
    ----------
    a : array_like
        Array containing numbers whose mean is desired. If `a` is not an
        array, a conversion is attempted.
    axis : {int, tuple of int, None}, optional
        Axis or axes along which the means are computed. The default is to compute
        the mean of the flattened array.
    dtype : data-type, optional
        Type to use in computing the mean.  For integer inputs, the default
        is `float64`; for inexact inputs, it is the same as the input
        dtype.
    out : ndarray, optional
        Alternate output array in which to place the result.  The default
        is ``None``; if provided, it must have the same shape as the
        expected output, but the type will be cast if necessary.
        See :ref:`ufuncs-output-type` for more details.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the original `a`.

        If the value is anything but the default, then
        `keepdims` will be passed through to the `mean` or `sum` methods
        of sub-classes of `ndarray`.  If the sub-classes methods
        does not implement `keepdims` any exceptions will be raised.
    where : array_like of bool, optional
        Elements to include in the mean. See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.22.0

    Returns
    -------
    m : ndarray, see dtype parameter above
        If `out=None`, returns a new array containing the mean values,
        otherwise a reference to the output array is returned. Nan is
        returned for slices that contain only NaNs.

    See Also
    --------
    average : Weighted average
    mean : Arithmetic mean taken while not ignoring NaNs
    var, nanvar

    Notes
    -----
    The arithmetic mean is the sum of the non-NaN elements along the axis
    divided by the number of non-NaN elements.

    Note that for floating-point input, the mean is computed using the same
    precision the input has.  Depending on the input data, this can cause
    the results to be inaccurate, especially for `float32`.  Specifying a
    higher-precision accumulator using the `dtype` keyword can alleviate
    this issue.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, np.nan], [3, 4]])
    >>> np.nanmean(a)
    2.6666666666666665
    >>> np.nanmean(a, axis=0)
    array([2.,  4.])
    >>> np.nanmean(a, axis=1)
    array([1.,  3.5]) # may vary

    """
    arr, mask = _replace_nan(a, 0)
    if mask is None:
        return np.mean(arr, axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                       where=where)

    if dtype is not None:
        dtype = np.dtype(dtype)
    if dtype is not None and not issubclass(dtype.type, np.inexact):
        raise TypeError("If a is inexact, then dtype must be inexact")
    if out is not None and not issubclass(out.dtype.type, np.inexact):
        raise TypeError("If a is inexact, then out must be inexact")

    cnt = np.sum(~mask, axis=axis, dtype=np.intp, keepdims=keepdims,
                 where=where)
    tot = np.sum(arr, axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                 where=where)
    avg = _divide_by_count(tot, cnt, out=out)

    isbad = (cnt == 0)
    if isbad.any():
        warnings.warn("Mean of empty slice", RuntimeWarning, stacklevel=2)
        # NaN is the only possible bad value, so no further
        # action is needed to handle bad results.
    return avg


def nanmean(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
            keepdims: bool = False, where: ArrayLike | None = None) -> Array:
  r"""Return the mean of the array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanmean`.

  Args:
    a: Input array.
    axis: int or sequence of ints, default=None. Axis along which the mean is
      computed. If None, the mean is computed along the flattened array.
    dtype: The type of the output array. Default=None.
    keepdims: bool, default=False. If True, reduced axes are left in the result
      with size 1.
    where: array of boolean dtype, default=None. The elements to be used in
      computing mean. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array containing the mean of array elements along the given axis, ignoring
    NaNs. If all elements along the given axis are NaNs, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmin`: Compute the minimum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmax`: Compute the maximum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nansum`: Compute the sum of array elements along a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanprod`: Compute the product of array elements along a
      given axis, ignoring NaNs.

  Examples:

    By default, ``jnp.nanmean`` computes the mean of elements along the flattened
    array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[2, nan, 4, 3],
    ...                [nan, -2, nan, 9],
    ...                [4, -7, 6, nan]])
    >>> jnp.nanmean(x)
    Array(2.375, dtype=float32)

    If ``axis=1``, mean will be computed along axis 1.

    >>> jnp.nanmean(x, axis=1)
    Array([3. , 3.5, 1. ], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.nanmean(x, axis=1, keepdims=True)
    Array([[3. ],
           [3.5],
           [1. ]], dtype=float32)

    ``where`` can be used to include only specific elements in computing the mean.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 0, 1, 1],
    ...                    [1, 1, 0, 1]], dtype=bool)
    >>> jnp.nanmean(x, axis=1, keepdims=True, where=where)
    Array([[ 3. ],
           [ 9. ],
           [-1.5]], dtype=float32)

    If ``where`` is ``False`` at all elements, ``jnp.nanmean`` returns ``nan``
    along the given axis.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.nanmean(x, axis=0, keepdims=True, where=where)
    Array([[nan, nan, nan, nan]], dtype=float32)
  """
  a = ensure_arraylike("nanmean", a)
  where = check_where("nanmean", where)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanmean is not supported.")
  if dtypes.issubdtype(a.dtype, np.bool_) or dtypes.issubdtype(a.dtype, np.integer):
    return mean(a, axis, dtype, out, keepdims, where=where)
  if dtype is None:
    dtype = dtypes.to_inexact_dtype(a.dtype)
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "mean")
  nan_mask = lax.bitwise_not(lax._isnan(a))
  normalizer = sum(nan_mask, axis=axis, dtype=dtype, keepdims=keepdims, where=where)
  td = lax.div(nansum(a, axis, dtype=dtype, keepdims=keepdims, where=where), normalizer)
  return td

