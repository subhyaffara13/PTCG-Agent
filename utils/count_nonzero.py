
def count_nonzero(a: ArrayLike, axis: AxisLike = None, *, keepdims: KeepDims = False):
    return a.count_nonzero(axis)


def count_nonzero(self, dim: DimsType | None = None):
    return (self != 0).sum(dim)


def count_nonzero(
    x: Array,
    axis: int | tuple[int, ...] | None = None,
    keepdims: py_bool = False,
) -> Array:
   result = cp.count_nonzero(x, axis)
   if keepdims:
       if axis is None:
            return cp.reshape(result, [1]*x.ndim)
       return cp.expand_dims(result, axis)
   return result


def count_nonzero(
    x: Array,
    axis: int | tuple[int, ...] | None = None,
    keepdims: py_bool = False,
) -> Array:
    # NOTE: this is currently incorrectly typed in numpy, but will be fixed in
    # numpy 2.2.5 and 2.3.0: https://github.com/numpy/numpy/pull/28750
    result = cast("Any", np.count_nonzero(x, axis=axis, keepdims=keepdims))  # pyright: ignore[reportArgumentType, reportCallIssue]
    if axis is None and not keepdims:
        return np.asarray(result)
    return result


def count_nonzero(
    x: Array,
    /,
    *,
    axis: int | tuple[int, ...] | None = None,
    keepdims: bool = False,
) -> Array:
    result = torch.count_nonzero(x, dim=axis)
    if keepdims:
        if isinstance(axis, int):
            return result.unsqueeze(axis)
        elif isinstance(axis, tuple):
            n_axis = [x.ndim + ax if ax < 0 else ax for ax in axis]
            sh = [1 if i in n_axis else x.shape[i] for i in range(x.ndim)]
            return torch.reshape(result, sh)
        return _axis_none_keepdims(result, x.ndim, keepdims)
    else:
        return result


def count_nonzero(
    x: Array,
    axis: int | None = None,
    keepdims: py_bool = False,
) -> Array:
    result = da.count_nonzero(x, axis)
    if keepdims:
        if axis is None:
            return da.reshape(result, [1] * x.ndim)
        return da.expand_dims(result, axis)
    return result


def count_nonzero(a, axis=None, *, keepdims=False):
    """
    Counts the number of non-zero values in the array ``a``.

    A non-zero value is one that evaluates to truthful in a boolean
    context, including any non-zero number and any string that
    is not empty. This function recursively counts how many elements
    in ``a`` (and its sub-arrays) are non-zero values.

    Parameters
    ----------
    a : array_like
        The array for which to count non-zeros.
    axis : int or tuple, optional
        Axis or tuple of axes along which to count non-zeros.
        Default is None, meaning that non-zeros will be counted
        along a flattened version of ``a``.
    keepdims : bool, optional
        If this is set to True, the axes that are counted are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

    Returns
    -------
    count : int or array of int
        Number of non-zero values in the array along a given axis.
        Otherwise, the total number of non-zero values in the array
        is returned.

    See Also
    --------
    nonzero : Return the coordinates of all the non-zero values.

    Examples
    --------
    >>> import numpy as np
    >>> np.count_nonzero(np.eye(4))
    np.int64(4)
    >>> a = np.array([[0, 1, 7, 0],
    ...               [3, 0, 2, 19]])
    >>> np.count_nonzero(a)
    np.int64(5)
    >>> np.count_nonzero(a, axis=0)
    array([1, 1, 2, 1])
    >>> np.count_nonzero(a, axis=1)
    array([2, 3])
    >>> np.count_nonzero(a, axis=1, keepdims=True)
    array([[2],
           [3]])
    """
    if axis is None and not keepdims:
        return multiarray.count_nonzero(a)

    a = asanyarray(a)

    # TODO: this works around .astype(bool) not working properly (gh-9847)
    if np.issubdtype(a.dtype, np.character):
        a_bool = a != a.dtype.type()
    else:
        a_bool = a.astype(np.bool, copy=False)

    return a_bool.sum(axis=axis, dtype=np.intp, keepdims=keepdims)


def count_nonzero(a: ArrayLike, axis: Axis = None,
                  keepdims: bool = False) -> Array:
  r"""Return the number of nonzero elements along a given axis.

  JAX implementation of :func:`numpy.count_nonzero`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      number of nonzeros are counted. If None, counts within the flattened array.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.

  Returns:
    An array with number of nonzeros elements along specified axis of the input.

  Examples:
    By default, ``jnp.count_nonzero`` counts the nonzero values along all axes.

    >>> x = jnp.array([[1, 0, 0, 0],
    ...                [0, 0, 1, 0],
    ...                [1, 1, 1, 0]])
    >>> jnp.count_nonzero(x)
    Array(5, dtype=int32)

    If ``axis=1``, counts along axis 1.

    >>> jnp.count_nonzero(x, axis=1)
    Array([1, 1, 3], dtype=int32)

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> jnp.count_nonzero(x, axis=1, keepdims=True)
    Array([[1],
           [1],
           [3]], dtype=int32)
  """
  a = ensure_arraylike("count_nonzero", a)
  return sum(lax.ne(a, lax._const(a, 0)), axis=axis,
             dtype=dtypes.default_int_dtype(), keepdims=keepdims)

