
def nanargmax(
    values: np.ndarray,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    mask: npt.NDArray[np.bool_] | None = None,
) -> int | np.ndarray:
    """
    Parameters
    ----------
    values : ndarray
    axis : int, optional
    skipna : bool, default True
    mask : ndarray[bool], optional
        nan-mask if known

    Returns
    -------
    result : int or ndarray[int]
        The index/indices  of max value in specified axis or -1 in the NA case

    Examples
    --------
    >>> from pandas.core import nanops
    >>> arr = np.array([1, 2, 3, np.nan, 4])
    >>> nanops.nanargmax(arr)
    np.int64(4)

    >>> arr = np.array(range(12), dtype=np.float64).reshape(4, 3)
    >>> arr[2:, 2] = np.nan
    >>> arr
    array([[ 0.,  1.,  2.],
           [ 3.,  4.,  5.],
           [ 6.,  7., nan],
           [ 9., 10., nan]])
    >>> nanops.nanargmax(arr, axis=1)
    array([2, 2, 1, 1])
    """
    values, mask = _get_values(values, True, fill_value_typ="-inf", mask=mask)
    result = values.argmax(axis)
    # error: Argument 1 to "_maybe_arg_null_out" has incompatible type "Any |
    # signedinteger[Any]"; expected "ndarray[Any, Any]"
    result = _maybe_arg_null_out(result, axis, mask, skipna)  # type: ignore[arg-type]
    return result


def nanargmax(a, axis=None, out=None, *, keepdims=np._NoValue):
    """
    Return the indices of the maximum values in the specified axis ignoring
    NaNs. For all-NaN slices ``ValueError`` is raised. Warning: the
    results cannot be trusted if a slice contains only NaNs and -Infs.


    Parameters
    ----------
    a : array_like
        Input data.
    axis : int, optional
        Axis along which to operate.  By default flattened input is used.
    out : array, optional
        If provided, the result will be inserted into this array. It should
        be of the appropriate shape and dtype.

        .. versionadded:: 1.22.0
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the array.

        .. versionadded:: 1.22.0

    Returns
    -------
    index_array : ndarray
        An array of indices or a single index value.

    See Also
    --------
    argmax, nanargmin

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[np.nan, 4], [2, 3]])
    >>> np.argmax(a)
    0
    >>> np.nanargmax(a)
    1
    >>> np.nanargmax(a, axis=0)
    array([1, 0])
    >>> np.nanargmax(a, axis=1)
    array([1, 1])

    """
    a, mask = _replace_nan(a, -np.inf)
    if mask is not None and mask.size:
        mask = np.all(mask, axis=axis)
        if np.any(mask):
            raise ValueError("All-NaN slice encountered")
    res = np.argmax(a, axis=axis, out=out, keepdims=keepdims)
    return res


def nanargmax(
    a: ArrayLike,
    axis: int | None = None,
    out: None = None,
    keepdims: bool | None = None,
) -> Array:
  """Return the index of the maximum value of an array, ignoring NaNs.

  JAX implementation of :func:`numpy.nanargmax`.

  Args:
    a: input array
    axis: optional integer specifying the axis along which to find the maximum
      value. If ``axis`` is not specified, ``a`` will be flattened.
    out: unused by JAX
    keepdims: if True, then return an array with the same number of dimensions
      as ``a``.

  Returns:
    an array containing the index of the maximum value along the specified axis.

  Note:
    In the case of an axis with all-NaN values, the returned index will be -1.
    This differs from the behavior of :func:`numpy.nanargmax`, which raises an error.

  See also:
    - :func:`jax.numpy.argmax`: return the index of the maximum value.
    - :func:`jax.numpy.nanargmin`: compute ``argmin`` while ignoring NaN values.

  Examples:
    >>> x = jnp.array([1, 3, 5, 4, jnp.nan])

    Using a standard :func:`~jax.numpy.argmax` leads to potentially unexpected results:

    >>> jnp.argmax(x)
    Array(4, dtype=int32)

    Using ``nanargmax`` returns the index of the maximum non-NaN value.

    >>> jnp.nanargmax(x)
    Array(2, dtype=int32)

    >>> x = jnp.array([[1, 3, jnp.nan],
    ...                [5, 4, jnp.nan]])
    >>> jnp.nanargmax(x, axis=1)
    Array([1, 0], dtype=int32)

    >>> jnp.nanargmax(x, axis=1, keepdims=True)
    Array([[1],
           [0]], dtype=int32)
  """
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanargmax is not supported.")
  a = util.ensure_arraylike("nanargmax", a)
  return _nanargmax(a, None if axis is None else operator.index(axis), keepdims=bool(keepdims))

