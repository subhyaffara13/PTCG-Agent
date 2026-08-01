
def nanargmin(
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
        The index/indices of min value in specified axis or -1 in the NA case

    Examples
    --------
    >>> from pandas.core import nanops
    >>> arr = np.array([1, 2, 3, np.nan, 4])
    >>> nanops.nanargmin(arr)
    np.int64(0)

    >>> arr = np.array(range(12), dtype=np.float64).reshape(4, 3)
    >>> arr[2:, 0] = np.nan
    >>> arr
    array([[ 0.,  1.,  2.],
           [ 3.,  4.,  5.],
           [nan,  7.,  8.],
           [nan, 10., 11.]])
    >>> nanops.nanargmin(arr, axis=1)
    array([0, 0, 1, 1])
    """
    values, mask = _get_values(values, True, fill_value_typ="+inf", mask=mask)
    result = values.argmin(axis)
    # error: Argument 1 to "_maybe_arg_null_out" has incompatible type "Any |
    # signedinteger[Any]"; expected "ndarray[Any, Any]"
    result = _maybe_arg_null_out(result, axis, mask, skipna)  # type: ignore[arg-type]
    return result


def nanargmin(a, axis=None, out=None, *, keepdims=np._NoValue):
    """
    Return the indices of the minimum values in the specified axis ignoring
    NaNs. For all-NaN slices ``ValueError`` is raised. Warning: the results
    cannot be trusted if a slice contains only NaNs and Infs.

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
    argmin, nanargmax

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[np.nan, 4], [2, 3]])
    >>> np.argmin(a)
    0
    >>> np.nanargmin(a)
    2
    >>> np.nanargmin(a, axis=0)
    array([1, 1])
    >>> np.nanargmin(a, axis=1)
    array([1, 0])

    """
    a, mask = _replace_nan(a, np.inf)
    if mask is not None and mask.size:
        mask = np.all(mask, axis=axis)
        if np.any(mask):
            raise ValueError("All-NaN slice encountered")
    res = np.argmin(a, axis=axis, out=out, keepdims=keepdims)
    return res


def nanargmin(
    a: ArrayLike,
    axis: int | None = None,
    out: None = None,
    keepdims: bool | None = None,
) -> Array:

  """Return the index of the minimum value of an array, ignoring NaNs.

  JAX implementation of :func:`numpy.nanargmin`.

  Args:
    a: input array
    axis: optional integer specifying the axis along which to find the maximum
      value. If ``axis`` is not specified, ``a`` will be flattened.
    out: unused by JAX
    keepdims: if True, then return an array with the same number of dimensions
      as ``a``.

  Returns:
    an array containing the index of the minimum value along the specified axis.

  Note:
    In the case of an axis with all-NaN values, the returned index will be -1.
    This differs from the behavior of :func:`numpy.nanargmin`, which raises an error.

  See also:
    - :func:`jax.numpy.argmin`: return the index of the minimum value.
    - :func:`jax.numpy.nanargmax`: compute ``argmax`` while ignoring NaN values.

  Examples:
    >>> x = jnp.array([jnp.nan, 3, 5, 4, 2])
    >>> jnp.nanargmin(x)
    Array(4, dtype=int32)

    >>> x = jnp.array([[1, 3, jnp.nan],
    ...                [5, 4, jnp.nan]])
    >>> jnp.nanargmin(x, axis=1)
    Array([0, 1], dtype=int32)

    >>> jnp.nanargmin(x, axis=1, keepdims=True)
    Array([[0],
           [1]], dtype=int32)
  """
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanargmin is not supported.")
  a = util.ensure_arraylike("nanargmin", a)
  return _nanargmin(a, None if axis is None else operator.index(axis), keepdims=bool(keepdims))

