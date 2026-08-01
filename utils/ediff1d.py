
def ediff1d(ary, to_end=None, to_begin=None):
    """
    The differences between consecutive elements of an array.

    Parameters
    ----------
    ary : array_like
        If necessary, will be flattened before the differences are taken.
    to_end : array_like, optional
        Number(s) to append at the end of the returned differences.
    to_begin : array_like, optional
        Number(s) to prepend at the beginning of the returned differences.

    Returns
    -------
    ediff1d : ndarray
        The differences. Loosely, this is ``ary.flat[1:] - ary.flat[:-1]``.

    See Also
    --------
    diff, gradient

    Notes
    -----
    When applied to masked arrays, this function drops the mask information
    if the `to_begin` and/or `to_end` parameters are used.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([1, 2, 4, 7, 0])
    >>> np.ediff1d(x)
    array([ 1,  2,  3, -7])

    >>> np.ediff1d(x, to_begin=-99, to_end=np.array([88, 99]))
    array([-99,   1,   2, ...,  -7,  88,  99])

    The returned array is always 1D.

    >>> y = [[1, 2, 4], [1, 6, 24]]
    >>> np.ediff1d(y)
    array([ 1,  2, -3,  5, 18])

    """
    conv = _array_converter(ary)
    # Convert to (any) array and ravel:
    ary = conv[0].ravel()

    # enforce that the dtype of `ary` is used for the output
    dtype_req = ary.dtype

    # fast track default case
    if to_begin is None and to_end is None:
        return ary[1:] - ary[:-1]

    if to_begin is None:
        l_begin = 0
    else:
        to_begin = np.asanyarray(to_begin)
        if not np.can_cast(to_begin, dtype_req, casting="same_kind"):
            raise TypeError("dtype of `to_begin` must be compatible "
                            "with input `ary` under the `same_kind` rule.")

        to_begin = to_begin.ravel()
        l_begin = len(to_begin)

    if to_end is None:
        l_end = 0
    else:
        to_end = np.asanyarray(to_end)
        if not np.can_cast(to_end, dtype_req, casting="same_kind"):
            raise TypeError("dtype of `to_end` must be compatible "
                            "with input `ary` under the `same_kind` rule.")

        to_end = to_end.ravel()
        l_end = len(to_end)

    # do the calculation in place and copy to_begin and to_end
    l_diff = max(len(ary) - 1, 0)
    result = np.empty_like(ary, shape=l_diff + l_begin + l_end)

    if l_begin > 0:
        result[:l_begin] = to_begin
    if l_end > 0:
        result[l_begin + l_diff:] = to_end
    np.subtract(ary[1:], ary[:-1], result[l_begin:l_begin + l_diff])

    return conv.wrap(result)


def ediff1d(arr, to_end=None, to_begin=None):
    """
    Compute the differences between consecutive elements of an array.

    This function is the equivalent of `numpy.ediff1d` that takes masked
    values into account, see `numpy.ediff1d` for details.

    See Also
    --------
    numpy.ediff1d : Equivalent function for ndarrays.

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.ma.array([1, 2, 4, 7, 0])
    >>> np.ma.ediff1d(arr)
    masked_array(data=[ 1,  2,  3, -7],
                 mask=False,
           fill_value=999999)

    """
    arr = ma.asanyarray(arr).flat
    ed = arr[1:] - arr[:-1]
    arrays = [ed]
    #
    if to_begin is not None:
        arrays.insert(0, to_begin)
    if to_end is not None:
        arrays.append(to_end)
    #
    if len(arrays) != 1:
        # We'll save ourselves a copy of a potentially large array in the common
        # case where neither to_begin or to_end was given.
        ed = hstack(arrays)
    #
    return ed


def ediff1d(ary: ArrayLike, to_end: ArrayLike | None = None,
            to_begin: ArrayLike | None = None) -> Array:
  """Compute the differences of the elements of the flattened array.

  JAX implementation of :func:`numpy.ediff1d`.

  Args:
    ary: input array or scalar.
    to_end: scalar or array, optional, default=None. Specifies the numbers to
      append to the resulting array.
    to_begin: scalar or array, optional, default=None. Specifies the numbers to
      prepend to the resulting array.

  Returns:
    An array containing the differences between the elements of the input array.

  Note:
    Unlike NumPy's implementation of ediff1d, :py:func:`jax.numpy.ediff1d` will
    not issue an error if casting ``to_end`` or ``to_begin`` to the type of
    ``ary`` loses precision.

  See also:
    - :func:`jax.numpy.diff`: Computes the n-th order difference between elements
      of the array along a given axis.
    - :func:`jax.numpy.cumsum`: Computes the cumulative sum of the elements of
      the array along a given axis.
    - :func:`jax.numpy.gradient`: Computes the gradient of an N-dimensional array.

  Examples:
    >>> a = jnp.array([2, 3, 5, 9, 1, 4])
    >>> jnp.ediff1d(a)
    Array([ 1,  2,  4, -8,  3], dtype=int32)
    >>> jnp.ediff1d(a, to_begin=-10)
    Array([-10,   1,   2,   4,  -8,   3], dtype=int32)
    >>> jnp.ediff1d(a, to_end=jnp.array([20, 30]))
    Array([ 1,  2,  4, -8,  3, 20, 30], dtype=int32)
    >>> jnp.ediff1d(a, to_begin=-10, to_end=jnp.array([20, 30]))
    Array([-10,   1,   2,   4,  -8,   3,  20,  30], dtype=int32)

    For array with ``ndim > 1``, the differences are computed after flattening
    the input array.

    >>> a1 = jnp.array([[2, -1, 4, 7],
    ...                 [3, 5, -6, 9]])
    >>> jnp.ediff1d(a1)
    Array([ -3,   5,   3,  -4,   2, -11,  15], dtype=int32)
    >>> a2 = jnp.array([2, -1, 4, 7, 3, 5, -6, 9])
    >>> jnp.ediff1d(a2)
    Array([ -3,   5,   3,  -4,   2, -11,  15], dtype=int32)
  """
  arr = util.ensure_arraylike("ediff1d", ary).ravel()
  result = lax.sub(arr[1:], arr[:-1])
  if to_begin is not None:
    to_begin = util.ensure_arraylike("ediff1d", to_begin)
    result = concatenate((ravel(to_begin.astype(arr.dtype)), result))
  if to_end is not None:
    to_end = util.ensure_arraylike("ediff1d", to_end)
    result = concatenate((result, ravel(to_end.astype(arr.dtype))))
  return result

