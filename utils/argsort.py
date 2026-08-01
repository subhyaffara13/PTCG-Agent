
def argsort(seq: Sequence[Any], *, reverse: bool = False) -> list[int]:
    getter = seq.__getitem__
    a_r = range(len(seq))
    # preserve original order for equal strides
    # e.g. if strides are [32, 8, 8, 1]
    # argsort -> [3, 2, 1, 0], rather than
    # [3, 1, 2, 0]
    # i.e. for equal strides in ascending order (reverse=False) an
    # inner dimension should come before an outer dimension, and vice versa
    # for descending
    sort_idx = list(sorted(a_r, key=getter, reverse=True))  # noqa: C413
    if not reverse:
        return list(reversed(sort_idx))
    return sort_idx


def argsort(a: ArrayLike, axis=-1, kind=None, order: NotImplementedType = None):
    a, axis, stable = _sort_helper(a, axis, kind, order)
    return torch.argsort(a, dim=axis, stable=stable)


def argsort(g: jit_utils.GraphContext, self, dim, descending, out=None):
    _, indices = symbolic_helper._sort_helper(
        g, self, dim, descending=descending, out=out
    )
    return indices


def argsort(
    x: Array,
    /,
    xp: Namespace,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    **kwargs: object,
) -> Array:
    # Note: this keyword argument is different, and the default is different.
    # We set it in kwargs like this because numpy.sort uses kind='quicksort'
    # as the default whereas cupy.sort uses kind=None.
    if stable:
        kwargs["kind"] = "stable"
    if not descending:
        res = xp.argsort(x, axis=axis, **kwargs)
    else:
        # As NumPy has no native descending sort, we imitate it here. Note that
        # simply flipping the results of xp.argsort(x, ...) would not
        # respect the relative order like it would in native descending sorts.
        res = xp.flip(
            xp.argsort(xp.flip(x, axis=axis), axis=axis, **kwargs),
            axis=axis,
        )
        # Rely on flip()/argsort() to validate axis
        normalised_axis = axis if axis >= 0 else x.ndim + axis
        max_i = x.shape[normalised_axis] - 1
        res = max_i - res
    return res


def argsort(
    x: Array,
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    **kwargs: object,
) -> Array:
    return torch.argsort(x, dim=axis, descending=descending, stable=stable, **kwargs)


def argsort(
    x: Array,
    /,
    *,
    axis: int = -1,
    descending: py_bool = False,
    stable: py_bool = True,
) -> Array:
    """
    Array API compatibility layer around the lack of argsort() in Dask.

    See the corresponding documentation in the array library and/or the array API
    specification for more details.

    Warnings
    --------
    This function temporarily rechunks the array along `axis` into a single chunk.
    This can be extremely inefficient and can lead to out-of-memory errors.
    """
    x, restore = _ensure_single_chunk(x, axis)

    meta_xp = array_namespace(x._meta)
    dtype = meta_xp.argsort(x._meta).dtype
    meta = meta_xp.astype(x._meta, dtype)
    x = da.map_blocks(
        meta_xp.argsort,
        x,
        axis=axis,
        meta=meta,
        dtype=dtype,
        descending=descending,
        stable=stable,
    )

    return restore(x)


def argsort(a, axis=np._NoValue, kind=None, order=None, endwith=True,
            fill_value=None, *, stable=None, descending=None):
    "Function version of the eponymous method."
    a = np.asanyarray(a)

    # 2017-04-11, Numpy 1.13.0, gh-8701: warn on axis default
    if axis is np._NoValue:
        axis = _deprecate_argsort_axis(a)

    if isinstance(a, MaskedArray):
        return a.argsort(axis=axis, kind=kind, order=order, endwith=endwith,
                         fill_value=fill_value, stable=stable, descending=descending)
    else:
        return a.argsort(axis=axis, kind=kind, order=order, stable=stable,
                         descending=descending)


def argsort(a, axis=-1, kind=None, order=None, *, stable=None, descending=np._NoValue):
    """
    Returns the indices that would sort an array.

    Perform an indirect sort along the given axis using the algorithm specified
    by the `kind` keyword. It returns an array of indices of the same shape as
    `a` that index data along the given axis in sorted order.

    Parameters
    ----------
    a : array_like
        Array to sort.
    axis : int or None, optional
        Axis along which to sort.  The default is -1 (the last axis). If None,
        the flattened array is used.
    kind : {'quicksort', 'mergesort', 'heapsort', 'stable'}, optional
        Sorting algorithm. The default is 'quicksort'. Note that both 'stable'
        and 'mergesort' use timsort under the covers and, in general, the
        actual implementation will vary with data type. The 'mergesort' option
        is retained for backwards compatibility.
    order : str or list of str, optional
        When `a` is an array with fields defined, this argument specifies
        which fields to compare first, second, etc.  A single field can
        be specified as a string, and not all fields need be specified,
        but unspecified fields will still be used, in the order in which
        they come up in the dtype, to break ties.
    stable : bool, optional
        Sort stability. If ``True``, the returned array will maintain
        the relative order of ``a`` values which compare as equal.
        If ``False`` or ``None``, this is not guaranteed. Internally,
        this option selects ``kind='stable'``. Default: ``None``.

        .. versionadded:: 2.0.0
    descending : bool, optional
        Sort order. If ``True``, the returned array will be sorted in
        descending order. If ``False`` or ``None``, the returned array will
        be sorted in ascending order. Values that are NaN are sorted to the
        end for both orders. Default: ``None``.

        .. versionadded:: 2.5.0

    Returns
    -------
    index_array : ndarray, int
        Array of indices that sort `a` along the specified `axis`.
        If `a` is one-dimensional, ``a[index_array]`` yields a sorted `a`.
        More generally, ``np.take_along_axis(a, index_array, axis=axis)``
        always yields the sorted `a`, irrespective of dimensionality.

    See Also
    --------
    sort : Describes sorting algorithms used.
    lexsort : Indirect stable sort with multiple keys.
    ndarray.sort : Inplace sort.
    argpartition : Indirect partial sort.
    take_along_axis : Apply ``index_array`` from argsort
                      to an array as if by calling sort.

    Notes
    -----
    See `sort` for notes on the different sorting algorithms.

    As of NumPy 1.4.0 `argsort` works with real/complex arrays containing
    nan values. The enhanced sort order is documented in `sort`.

    Examples
    --------
    One dimensional array:

    >>> import numpy as np
    >>> x = np.array([3, 1, 2])
    >>> np.argsort(x)
    array([1, 2, 0])

    Two-dimensional array:

    >>> x = np.array([[0, 3], [2, 2]])
    >>> x
    array([[0, 3],
           [2, 2]])

    >>> ind = np.argsort(x, axis=0)  # sorts along first axis (down)
    >>> ind
    array([[0, 1],
           [1, 0]])
    >>> np.take_along_axis(x, ind, axis=0)  # same as np.sort(x, axis=0)
    array([[0, 2],
           [2, 3]])

    >>> ind = np.argsort(x, axis=1)  # sorts along last axis (across)
    >>> ind
    array([[0, 1],
           [0, 1]])
    >>> np.take_along_axis(x, ind, axis=1)  # same as np.sort(x, axis=1)
    array([[0, 3],
           [2, 2]])

    Indices of the sorted elements of an N-dimensional array:

    >>> ind = np.unravel_index(np.argsort(x, axis=None), x.shape)
    >>> ind
    (array([0, 1, 1, 0]), array([0, 0, 1, 1]))
    >>> x[ind]  # same as np.sort(x, axis=None)
    array([0, 2, 2, 3])

    Sorting with keys:

    >>> x = np.array([(1, 0), (0, 1)], dtype=[('x', '<i4'), ('y', '<i4')])
    >>> x
    array([(1, 0), (0, 1)],
          dtype=[('x', '<i4'), ('y', '<i4')])

    >>> np.argsort(x, order=('x','y'))
    array([1, 0])

    >>> np.argsort(x, order=('y','x'))
    array([0, 1])

    """
    # Sanitize for backward-compatibility
    if descending is not np._NoValue:
        return _wrapfunc(
            a,
            "argsort",
            axis=axis,
            kind=kind,
            order=order,
            stable=stable,
            descending=descending,
        )
    return _wrapfunc(
        a,
        "argsort",
        axis=axis,
        kind=kind,
        order=order,
        stable=stable,
    )


def argsort(
    a: ArrayLike,
    axis: int | None = -1,
    *,
    kind: None = None,
    order: None = None,
    stable: bool = True,
    descending: bool = False,
    dtype: DTypeLike | None = None,
) -> Array:
  """Return indices that sort an array.

  JAX implementation of :func:`numpy.argsort`.

  Args:
    a: array to sort
    axis: integer axis along which to sort. Defaults to ``-1``, i.e. the last
      axis. If ``None``, then ``a`` is flattened before being sorted.
    stable: boolean specifying whether a stable sort should be used. Default=True.
    descending: boolean specifying whether to sort in descending order. Default=False.
    kind: deprecated; instead specify sort algorithm using stable=True or stable=False.
    order: not supported by JAX
    dtype: optionally specify the dtype of the resulting indices. If not specified,
      the default integer dtype will be used.

  Returns:
    Array of indices that sort an array. Returned array will be of shape ``a.shape``
    (if ``axis`` is an integer) or of shape ``(a.size,)`` (if ``axis`` is None).

  Examples:
    Simple 1-dimensional sort

    >>> x = jnp.array([1, 3, 5, 4, 2, 1])
    >>> indices = jnp.argsort(x)
    >>> indices
    Array([0, 5, 4, 1, 3, 2], dtype=int32)
    >>> x[indices]
    Array([1, 1, 2, 3, 4, 5], dtype=int32)

    Sort along the last axis of an array:

    >>> x = jnp.array([[2, 1, 3],
    ...                [6, 4, 3]])
    >>> indices = jnp.argsort(x, axis=1)
    >>> indices
    Array([[1, 0, 2],
           [2, 1, 0]], dtype=int32)
    >>> jnp.take_along_axis(x, indices, axis=1)
    Array([[1, 2, 3],
           [3, 4, 6]], dtype=int32)


  See also:
    - :func:`jax.numpy.sort`: return sorted values directly.
    - :func:`jax.numpy.lexsort`: lexicographical sort of multiple arrays.
    - :func:`jax.lax.sort`: lower-level function wrapping XLA's Sort operator.
  """
  arr = util.ensure_arraylike("argsort", a)
  if kind is not None:
    raise TypeError("'kind' argument to argsort is not supported. Use"
                    " stable=True or stable=False to specify sort stability.")
  if order is not None:
    raise TypeError("'order' argument to argsort is not supported.")
  if axis is None:
    arr = arr.ravel()
    axis = 0
  dimension = canonicalize_axis(axis, arr.ndim)
  if dtype is not None:
    idx_dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "argsort")
  else:
    idx_dtype = lax_utils.int_dtype_for_dim(arr.shape[dimension], signed=True)
    # We'd give the correct output values with int32, but use the default dtype to
    # match NumPy type semantics if x64 mode is enabled for now.
    if idx_dtype == np.dtype(np.int32):
      idx_dtype = dtypes.default_int_dtype()
  iota = lax.broadcasted_iota(idx_dtype, arr.shape, dimension,
                              out_sharding=core.typeof(arr).sharding)
  # For stable descending sort, we reverse the array and indices to ensure that
  # duplicates remain in their original order when the final indices are reversed.
  # For non-stable descending sort, we can avoid these extra operations.
  if descending and stable:
    arr = lax.rev(arr, dimensions=[dimension])
    iota = lax.rev(iota, dimensions=[dimension])
  _, indices = lax.sort_key_val(arr, iota, dimension=dimension, is_stable=stable)
  return lax.rev(indices, dimensions=[dimension]) if descending else indices

