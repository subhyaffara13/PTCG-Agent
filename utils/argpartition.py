
def argpartition(
    a: Array,
    kth: int,
    /,
    axis: int | None = -1,
    *,
    xp: ModuleType | None = None,
) -> Array:
    """
    Perform an indirect partition along the given axis.

    It returns an array of indices of the same shape as `a` that
    index data along the given axis in partitioned order.

    Parameters
    ----------
    a : Array
        Input array.
    kth : int
        Element index to partition by.
    axis : int, optional
        Axis along which to partition. The default is ``-1`` (the last axis).
        If ``None``, the flattened array is used.
    xp : array_namespace, optional
        The standard-compatible namespace for `x`. Default: infer.

    Returns
    -------
    index_array
        Array of indices that partition `a` along the specified axis.

    Notes
    -----
    If `xp` implements ``argpartition`` or an equivalent function
    e.g. ``topk`` for torch), complexity will likely be O(n).
    If not, this function simply calls ``xp.argsort`` and complexity is O(n log n).
    """
    # Validate inputs.
    if xp is None:
        xp = array_namespace(a)
    if is_pydata_sparse_namespace(xp):
        msg = "Not implemented for sparse backend: no argsort"
        raise NotImplementedError(msg)
    if a.ndim < 1:
        msg = "`a` must be at least 1-dimensional"
        raise TypeError(msg)
    if axis is None:
        return argpartition(xp.reshape(a, (-1,)), kth, axis=0, xp=xp)
    (size,) = eager_shape(a, axis)
    if not (0 <= kth < size):
        msg = f"kth(={kth}) out of bounds [0 {size})"
        raise ValueError(msg)

    # Delegate where possible.
    if is_numpy_namespace(xp) or is_cupy_namespace(xp) or is_jax_namespace(xp):
        return xp.argpartition(a, kth, axis=axis)

    # Use top-k when possible:
    if is_torch_namespace(xp):
        # see `partition` above for commented details of those steps:
        if not (axis == -1 or axis == a.ndim - 1):
            a = xp.transpose(a, axis, -1)

        ranks = xp.arange(a.shape[-1]).expand_as(a)
        out = xp.empty_like(ranks)

        split_value, indices = xp.kthvalue(a, kth + 1, keepdim=True)
        del indices  # indices won't be used => del ASAP to reduce peak memory usage

        mask_src = a < split_value
        n_left = mask_src.sum(dim=-1, keepdim=True)
        mask_dest = ranks < n_left
        out[mask_dest] = ranks[mask_src]

        mask_src = a == split_value
        n_left += mask_src.sum(dim=-1, keepdim=True)
        mask_dest ^= ranks < n_left
        out[mask_dest] = ranks[mask_src]

        mask_src = a > split_value
        mask_dest = ranks >= n_left
        out[mask_dest] = ranks[mask_src]

        if not (axis == -1 or axis == a.ndim - 1):
            out = xp.transpose(out, axis, -1)
        return out

    # Note: dask topk/argtopk sort the return values, so it's
    # not much more efficient than sorting everything when
    # kth is not small compared to x.size

    return _funcs.argpartition(a, kth, axis=axis, xp=xp)


def argpartition(  # numpydoc ignore=PR01,RT01
    x: Array,
    kth: int,  # noqa: ARG001
    /,
    axis: int = -1,
    *,
    xp: ModuleType,
) -> Array:
    """See docstring in `array_api_extra._delegation.py`."""
    return xp.argsort(x, axis=axis, stable=False)


def argpartition(a, kth, axis=-1, kind='introselect', order=None):
    """
    Perform an indirect partition along the given axis using the
    algorithm specified by the `kind` keyword. It returns an array of
    indices of the same shape as `a` that index data along the given
    axis in partitioned order.

    Parameters
    ----------
    a : array_like
        Array to sort.
    kth : int or sequence of ints
        Element index to partition by. The k-th element will be in its
        final sorted position and all smaller elements will be moved
        before it and all larger elements behind it. The order of all
        elements in the partitions is undefined. If provided with a
        sequence of k-th it will partition all of them into their sorted
        position at once.

    axis : int or None, optional
        Axis along which to sort. The default is -1 (the last axis). If
        None, the flattened array is used.
    kind : {'introselect'}, optional
        Selection algorithm. Default is 'introselect'
    order : str or list of str, optional
        When `a` is an array with fields defined, this argument
        specifies which fields to compare first, second, etc. A single
        field can be specified as a string, and not all fields need be
        specified, but unspecified fields will still be used, in the
        order in which they come up in the dtype, to break ties.

    Returns
    -------
    index_array : ndarray, int
        Array of indices that partition `a` along the specified axis.
        If `a` is one-dimensional, ``a[index_array]`` yields a partitioned `a`.
        More generally, ``np.take_along_axis(a, index_array, axis=axis)``
        always yields the partitioned `a`, irrespective of dimensionality.

    See Also
    --------
    partition : Describes partition algorithms used.
    ndarray.partition : Inplace partition.
    argsort : Full indirect sort.
    take_along_axis : Apply ``index_array`` from argpartition
                      to an array as if by calling partition.

    Notes
    -----
    The returned indices are not guaranteed to be sorted according to
    the values. Furthermore, the default selection algorithm ``introselect``
    is unstable, and hence the returned indices are not guaranteed
    to be the earliest/latest occurrence of the element.

    `argpartition` works for real/complex inputs with nan values,
    see `partition` for notes on the enhanced sort order and
    different selection algorithms.

    Examples
    --------
    One dimensional array:

    >>> import numpy as np
    >>> x = np.array([3, 4, 2, 1])
    >>> x[np.argpartition(x, 3)]
    array([2, 1, 3, 4]) # may vary
    >>> x[np.argpartition(x, (1, 3))]
    array([1, 2, 3, 4]) # may vary

    >>> x = [3, 4, 2, 1]
    >>> np.array(x)[np.argpartition(x, 3)]
    array([2, 1, 3, 4]) # may vary

    Multi-dimensional array:

    >>> x = np.array([[3, 4, 2], [1, 3, 1]])
    >>> index_array = np.argpartition(x, kth=1, axis=-1)
    >>> # below is the same as np.partition(x, kth=1)
    >>> np.take_along_axis(x, index_array, axis=-1)
    array([[2, 3, 4],
           [1, 1, 3]])

    """
    return _wrapfunc(a, 'argpartition', kth, axis=axis, kind=kind, order=order)


def argpartition(a: ArrayLike, kth: int, axis: int = -1) -> Array:
  """Returns indices that partially sort an array.

  JAX implementation of :func:`numpy.argpartition`. The JAX version differs from
  NumPy in the treatment of NaN entries: NaNs which have the negative bit set are
  sorted to the beginning of the array.

  Args:
    a: array to be partitioned.
    kth: static integer index about which to partition the array.
    axis: static integer axis along which to partition the array; default is -1.

  Returns:
    Indices which partition ``a`` at the ``kth`` value along ``axis``. The entries
    before ``kth`` are indices of values smaller than ``take(a, kth, axis)``, and
    entries after ``kth`` are indices of values larger than ``take(a, kth, axis)``

  Note:
    The JAX version requires the ``kth`` argument to be a static integer rather than
    a general array. This is implemented via two calls to :func:`jax.lax.top_k`. If
    you're only accessing the top or bottom k values of the output, it may be more
    efficient to call :func:`jax.lax.top_k` directly.

  See Also:
    - :func:`jax.numpy.partition`: direct partial sort
    - :func:`jax.numpy.argsort`: full indirect sort
    - :func:`jax.lax.top_k`: directly find the top k entries
    - :func:`jax.lax.approx_max_k`: compute the approximate top k entries
    - :func:`jax.lax.approx_min_k`: compute the approximate bottom k entries

  Examples:
    >>> x = jnp.array([6, 8, 4, 3, 1, 9, 7, 5, 2, 3])
    >>> kth = 4
    >>> idx = jnp.argpartition(x, kth)
    >>> idx
    Array([4, 8, 3, 9, 2, 0, 1, 5, 6, 7], dtype=int32)

    The result is a sequence of indices that partially sort the input. All indices
    before ``kth`` are of values smaller than the pivot value, and all indices
    after ``kth`` are of values larger than the pivot value:

    >>> x_partitioned = x[idx]
    >>> smallest_values = x_partitioned[:kth]
    >>> pivot_value = x_partitioned[kth]
    >>> largest_values = x_partitioned[kth + 1:]
    >>> print(smallest_values, pivot_value, largest_values)
    [1 2 3 3] 4 [6 8 9 7 5]

    Notice that among ``smallest_values`` and ``largest_values``, the returned
    order is arbitrary and implementation-dependent.
  """
  # TODO(jakevdp): handle NaN values like numpy.
  arr = util.ensure_arraylike("partition", a)
  if dtypes.issubdtype(arr.dtype, np.complexfloating):
    raise NotImplementedError("jnp.argpartition for complex dtype is not implemented.")
  axis = canonicalize_axis(axis, arr.ndim)
  kth = canonicalize_axis(kth, arr.shape[axis])

  arr = arr.swapaxes(axis, -1)
  if dtypes.isdtype(arr.dtype, "unsigned integer"):
    # Here, we apply a trick to handle correctly 0 values for unsigned integers
    bottom_ind = lax.top_k(-(arr + 1), kth + 1)[1]
  else:
    bottom_ind = lax.top_k(-arr, kth + 1)[1]

  # To avoid issues with duplicate values, we compute the top indices via a proxy
  set_to_zero = lambda a, i: a.at[i].set(0)
  for _ in range(arr.ndim - 1):
    set_to_zero = api.vmap(set_to_zero)
  proxy = set_to_zero(lax.full(arr.shape, 1.0), bottom_ind)
  top_ind = lax.top_k(proxy, arr.shape[-1] - kth - 1)[1]
  out = lax.concatenate([bottom_ind, top_ind], dimension=arr.ndim - 1)
  return out.swapaxes(-1, axis)

