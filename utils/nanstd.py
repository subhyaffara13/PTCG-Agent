
def nanstd(
    values,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    ddof: int = 1,
    mask=None,
):
    """
    Compute the standard deviation along given axis while ignoring NaNs

    Parameters
    ----------
    values : ndarray
    axis : int, optional
    skipna : bool, default True
    ddof : int, default 1
        Delta Degrees of Freedom. The divisor used in calculations is N - ddof,
        where N represents the number of elements.
    mask : ndarray[bool], optional
        nan-mask if known

    Returns
    -------
    result : float
        Unless input is a float array, in which case use the same
        precision as the input array.

    Examples
    --------
    >>> from pandas.core import nanops
    >>> s = pd.Series([1, np.nan, 2, 3])
    >>> nanops.nanstd(s.values)
    1.0
    """
    if values.dtype.kind == "M":
        unit = np.datetime_data(values.dtype)[0]
        values = values.view(f"m8[{unit}]")

    orig_dtype = values.dtype
    values, mask = _get_values(values, skipna, mask=mask)

    result = np.sqrt(nanvar(values, axis=axis, skipna=skipna, ddof=ddof, mask=mask))
    return _wrap_results(result, orig_dtype)


def nanstd(a, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue,
           *, where=np._NoValue, mean=np._NoValue, correction=np._NoValue):
    """
    Compute the standard deviation along the specified axis, while
    ignoring NaNs.

    Returns the standard deviation, a measure of the spread of a
    distribution, of the non-NaN array elements. The standard deviation is
    computed for the flattened array by default, otherwise over the
    specified axis.

    For all-NaN slices or slices with zero degrees of freedom, NaN is
    returned and a `RuntimeWarning` is raised.

    Parameters
    ----------
    a : array_like
        Calculate the standard deviation of the non-NaN values.
    axis : {int, tuple of int, None}, optional
        Axis or axes along which the standard deviation is computed. The default is
        to compute the standard deviation of the flattened array.
    dtype : dtype, optional
        Type to use in computing the standard deviation. For arrays of
        integer type the default is float64, for arrays of float types it
        is the same as the array type.
    out : ndarray, optional
        Alternative output array in which to place the result. It must have
        the same shape as the expected output but the type (of the
        calculated values) will be cast if necessary.
    ddof : {int, float}, optional
        Means Delta Degrees of Freedom.  The divisor used in calculations
        is ``N - ddof``, where ``N`` represents the number of non-NaN
        elements.  By default `ddof` is zero.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the original `a`.

        If this value is anything but the default it is passed through
        as-is to the relevant functions of the sub-classes.  If these
        functions do not have a `keepdims` kwarg, a RuntimeError will
        be raised.
    where : array_like of bool, optional
        Elements to include in the standard deviation.
        See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.22.0

    mean : array_like, optional
        Provide the mean to prevent its recalculation. The mean should have
        a shape as if it was calculated with ``keepdims=True``.
        The axis for the calculation of the mean should be the same as used in
        the call to this std function.

        .. versionadded:: 2.0.0

    correction : {int, float}, optional
        Array API compatible name for the ``ddof`` parameter. Only one of them
        can be provided at the same time.

        .. versionadded:: 2.0.0

    Returns
    -------
    standard_deviation : ndarray, see dtype parameter above.
        If `out` is None, return a new array containing the standard
        deviation, otherwise return a reference to the output array. If
        ddof is >= the number of non-NaN elements in a slice or the slice
        contains only NaNs, then the result for that slice is NaN.

    See Also
    --------
    var, mean, std
    nanvar, nanmean
    :ref:`ufuncs-output-type`

    Notes
    -----
    The standard deviation is the square root of the average of the squared
    deviations from the mean: ``std = sqrt(mean(abs(x - x.mean())**2))``.

    The average squared deviation is normally calculated as
    ``x.sum() / N``, where ``N = len(x)``.  If, however, `ddof` is
    specified, the divisor ``N - ddof`` is used instead. In standard
    statistical practice, ``ddof=1`` provides an unbiased estimator of the
    variance of the infinite population. ``ddof=0`` provides a maximum
    likelihood estimate of the variance for normally distributed variables.
    The standard deviation computed in this function is the square root of
    the estimated variance, so even with ``ddof=1``, it will not be an
    unbiased estimate of the standard deviation per se.

    Note that, for complex numbers, `std` takes the absolute value before
    squaring, so that the result is always real and nonnegative.

    For floating-point input, the *std* is computed using the same
    precision the input has. Depending on the input data, this can cause
    the results to be inaccurate, especially for float32 (see example
    below).  Specifying a higher-accuracy accumulator using the `dtype`
    keyword can alleviate this issue.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, np.nan], [3, 4]])
    >>> np.nanstd(a)
    1.247219128924647
    >>> np.nanstd(a, axis=0)
    array([1., 0.])
    >>> np.nanstd(a, axis=1)
    array([0.,  0.5]) # may vary

    """
    var = nanvar(a, axis=axis, dtype=dtype, out=out, ddof=ddof,
                 keepdims=keepdims, where=where, mean=mean,
                 correction=correction)
    if isinstance(var, np.ndarray):
        std = np.sqrt(var, out=var)
    elif hasattr(var, 'dtype'):
        std = var.dtype.type(np.sqrt(var))
    else:
        std = np.sqrt(var)
    return std


def nanstd(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
           ddof: int = 0, keepdims: bool = False,
           where: ArrayLike | None = None, mean: ArrayLike | None = None) -> Array:
  r"""Compute the standard deviation along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanstd`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      standard deviation is computed. If None, standard deviaiton is computed
      along flattened array.
    dtype: The type of the output array. Default=None.
    ddof: int, default=0. Degrees of freedom. The divisor in the standard deviation
      computation is ``N-ddof``, ``N`` is number of elements along given axis.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: optional, boolean array, default=None. The elements to be used in the
      standard deviation. Array should be broadcast compatible to the input.
    mean: optional, mean of the input array, computed along the given axis.
      If provided, it will be used to compute the standard deviation instead of
      computing it from the input array. If specified, mean must be broadcast-compatible
      with the input array. In the general case, this can be achieved by computing the mean with
      ``keepdims=True`` and ``axis`` matching this function's ``axis`` argument.
    out: Unused by JAX.

  Returns:
    An array containing the standard deviation of array elements along the given
    axis. If all elements along the given axis are NaNs, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements over a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanvar`: Compute the variance along the given axis, ignoring
      NaNs values.
    - :func:`jax.numpy.std`: Computed the standard deviation along the given axis.

  Examples:
    By default, ``jnp.nanstd`` computes the standard deviation along flattened array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[3, nan, 4, 5],
    ...                [nan, 2, nan, 7],
    ...                [2, 1, 6, nan]])
    >>> jnp.nanstd(x)
    Array(1.9843135, dtype=float32)

    If ``axis=0``, computes standard deviation along axis 0.

    >>> jnp.nanstd(x, axis=0)
    Array([0.5, 0.5, 1. , 1. ], dtype=float32)

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> jnp.nanstd(x, axis=0, keepdims=True)
    Array([[0.5, 0.5, 1. , 1. ]], dtype=float32)

    If ``ddof=1``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.nanstd(x, axis=0, keepdims=True, ddof=1))
    [[0.71 0.71 1.41 1.41]]

    To include specific elements of the array to compute standard deviation, you
    can use ``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 1, 0, 1],
    ...                  [1, 1, 0, 1]], dtype=bool)
    >>> jnp.nanstd(x, axis=0, keepdims=True, where=where)
    Array([[0.5, 0.5, 0. , 0. ]], dtype=float32)
  """
  a = ensure_arraylike("nanstd", a)
  where = check_where("nanstd", where)
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "nanstd")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanstd is not supported.")
  return lax.sqrt(nanvar(a, axis=axis, dtype=dtype, ddof=ddof,
                         keepdims=keepdims, where=where, mean=mean))

