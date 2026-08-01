
def take_along_axis(arr: ArrayLike, indices: ArrayLike, axis):
    (arr,), axis = _util.axis_none_flatten(arr, axis=axis)
    axis = _util.normalize_axis_index(axis, arr.ndim)
    return torch.take_along_dim(arr, indices, axis)


def take_along_axis(x: Array, indices: Array, /, *, axis: int = -1) -> Array:
    return cp.take_along_axis(x, indices, axis=axis)


def take_along_axis(x: Array, indices: Array, /, *, axis: int = -1) -> Array:
    return np.take_along_axis(x, indices, axis=axis)


def take_along_axis(x: Array, indices: Array, /, *, axis: int = -1) -> Array:
    # torch does not support negative indices,
    # see https://github.com/pytorch/pytorch/issues/146211
    return torch.take_along_dim(
        x,
        torch.where(indices < 0, indices + x.shape[axis], indices),
        dim=axis
    )


def take_along_axis(arr, indices, axis=-1):
    """
    Take values from the input array by matching 1d index and data slices.

    This iterates over matching 1d slices oriented along the specified axis in
    the index and data arrays, and uses the former to look up values in the
    latter. These slices can be different lengths.

    Functions returning an index along an axis, like `argsort` and
    `argpartition`, produce suitable indices for this function.

    Parameters
    ----------
    arr : ndarray (Ni..., M, Nk...)
        Source array
    indices : ndarray (Ni..., J, Nk...)
        Indices to take along each 1d slice of ``arr``. This must match the
        dimension of ``arr``, but dimensions Ni and Nj only need to broadcast
        against ``arr``.
    axis : int or None, optional
        The axis to take 1d slices along. If axis is None, the input array is
        treated as if it had first been flattened to 1d, for consistency with
        `sort` and `argsort`.

        .. versionchanged:: 2.3
            The default value is now ``-1``.

    Returns
    -------
    out: ndarray (Ni..., J, Nk...)
        The indexed result.

    Notes
    -----
    This is equivalent to (but faster than) the following use of `ndindex` and
    `s_`, which sets each of ``ii`` and ``kk`` to a tuple of indices::

        Ni, M, Nk = a.shape[:axis], a.shape[axis], a.shape[axis+1:]
        J = indices.shape[axis]  # Need not equal M
        out = np.empty(Ni + (J,) + Nk)

        for ii in ndindex(Ni):
            for kk in ndindex(Nk):
                a_1d       = a      [ii + s_[:,] + kk]
                indices_1d = indices[ii + s_[:,] + kk]
                out_1d     = out    [ii + s_[:,] + kk]
                for j in range(J):
                    out_1d[j] = a_1d[indices_1d[j]]

    Equivalently, eliminating the inner loop, the last two lines would be::

                out_1d[:] = a_1d[indices_1d]

    See Also
    --------
    take : Take along an axis, using the same indices for every 1d slice
    put_along_axis :
        Put values into the destination array by matching 1d index and data slices

    Examples
    --------
    >>> import numpy as np

    For this sample array

    >>> a = np.array([[10, 30, 20], [60, 40, 50]])

    We can sort either by using sort directly, or argsort and this function

    >>> np.sort(a, axis=1)
    array([[10, 20, 30],
           [40, 50, 60]])
    >>> ai = np.argsort(a, axis=1)
    >>> ai
    array([[0, 2, 1],
           [1, 2, 0]])
    >>> np.take_along_axis(a, ai, axis=1)
    array([[10, 20, 30],
           [40, 50, 60]])

    The same works for max and min, if you maintain the trivial dimension
    with ``keepdims``:

    >>> np.max(a, axis=1, keepdims=True)
    array([[30],
           [60]])
    >>> ai = np.argmax(a, axis=1, keepdims=True)
    >>> ai
    array([[1],
           [0]])
    >>> np.take_along_axis(a, ai, axis=1)
    array([[30],
           [60]])

    If we want to get the max and min at the same time, we can stack the
    indices first

    >>> ai_min = np.argmin(a, axis=1, keepdims=True)
    >>> ai_max = np.argmax(a, axis=1, keepdims=True)
    >>> ai = np.concatenate([ai_min, ai_max], axis=1)
    >>> ai
    array([[0, 1],
           [1, 0]])
    >>> np.take_along_axis(a, ai, axis=1)
    array([[10, 30],
           [40, 60]])
    """
    # normalize inputs
    if axis is None:
        if indices.ndim != 1:
            raise ValueError(
                'when axis=None, `indices` must have a single dimension.')
        arr = np.array(arr.flat)
        axis = 0
    else:
        axis = normalize_axis_index(axis, arr.ndim)

    # use the fancy index
    return arr[_make_along_axis_idx(arr.shape, indices, axis)]


def take_along_axis(
    arr: ArrayLike,
    indices: ArrayLike,
    axis: int | None = -1,
    mode: str | slicing.GatherScatterMode | None = None,
    fill_value: StaticScalar | None = None,
    *,
    wrap_negative_indices: bool | None = None,
) -> Array:
  """Take elements from an array.

  JAX implementation of :func:`numpy.take_along_axis`, implemented in
  terms of :func:`jax.lax.gather`. JAX's behavior differs from NumPy
  in the case of out-of-bound indices; see the ``mode`` parameter below.

  Args:
    a: array from which to take values.
    indices: array of integer indices. If ``axis`` is ``None``, must be
      one-dimensional. If ``axis`` is not None, must have ``a.ndim ==
      indices.ndim``, and ``a`` must be broadcast-compatible with ``indices``
      along dimensions other than ``axis``.
    axis: the axis along which to take values. If not specified, the array will
      be flattened before indexing is applied.
    mode: Out-of-bounds indexing mode, either ``"fill"`` or ``"clip"``. The
      default ``mode="fill"`` returns invalid values (e.g. NaN) for out-of
      bounds indices. For more discussion of ``mode`` options, see
      :attr:`jax.numpy.ndarray.at`.
    wrap_negative_indices: Whether to wrap negative indices to positive like
      Numpy. If unset, defaults to a legacy behavior (wrapping unless the
      indexing mode is 'promise_in_bounds'), but this will likely be removed and
      the default changed to True in the future, so do not depend on it.

  Returns:
    Array of values extracted from ``a``.

  See also:
    - :attr:`jax.numpy.ndarray.at`: take values via indexing syntax.
    - :func:`jax.numpy.take`: take the same indices along every axis slice.

  Examples:
    >>> x = jnp.array([[1., 2., 3.],
    ...                [4., 5., 6.]])
    >>> indices = jnp.array([[0, 2],
    ...                      [1, 0]])
    >>> jnp.take_along_axis(x, indices, axis=1)
    Array([[1., 3.],
           [5., 4.]], dtype=float32)
    >>> x[jnp.arange(2)[:, None], indices]  # equivalent via indexing syntax
    Array([[1., 3.],
           [5., 4.]], dtype=float32)

    Out-of-bound indices fill with invalid values. For float inputs, this is
    `NaN`:

    >>> indices = jnp.array([[1, 0, 2]])
    >>> jnp.take_along_axis(x, indices, axis=0)
    Array([[ 4.,  2., nan]], dtype=float32)
    >>> x.at[indices, jnp.arange(3)].get(
    ...     mode='fill', fill_value=jnp.nan)  # equivalent via indexing syntax
    Array([[ 4.,  2., nan]], dtype=float32)

    ``take_along_axis`` is helpful for extracting values from multi-dimensional
    argsorts and arg reductions. For, here we compute :func:`~jax.numpy.argsort`
    indices along an axis, and use ``take_along_axis`` to construct the sorted
    array:

    >>> x = jnp.array([[5, 3, 4],
    ...                [2, 7, 6]])
    >>> indices = jnp.argsort(x, axis=1)
    >>> indices
    Array([[1, 2, 0],
           [0, 2, 1]], dtype=int32)
    >>> jnp.take_along_axis(x, indices, axis=1)
    Array([[3, 4, 5],
           [2, 6, 7]], dtype=int32)

    Similarly, we can use :func:`~jax.numpy.argmin` with ``keepdims=True`` and
    use ``take_along_axis`` to extract the minimum value:

    >>> idx = jnp.argmin(x, axis=1, keepdims=True)
    >>> idx
    Array([[1],
           [0]], dtype=int32)
    >>> jnp.take_along_axis(x, idx, axis=1)
    Array([[3],
           [2]], dtype=int32)
  """
  a, indices = util.ensure_arraylike("take_along_axis", arr, indices)
  index_dtype = indices.dtype
  idx_shape = np.shape(indices)
  if not dtypes.issubdtype(index_dtype, np.integer):
    raise TypeError("take_along_axis indices must be of integer type, got "
                    f"{index_dtype}")
  if axis is None:
    if np.ndim(indices) != 1:
      msg = "take_along_axis indices must be 1D if axis=None, got shape {}"
      raise ValueError(msg.format(idx_shape))
    a = a.ravel()
    axis = 0
  rank = a.ndim
  if rank != np.ndim(indices):
    msg = "indices and arr must have the same number of dimensions; {} vs. {}"
    raise ValueError(msg.format(np.ndim(indices), a.ndim))
  axis_int = canonicalize_axis(axis, rank)

  def replace(tup, val):
    lst = list(tup)
    lst[axis_int] = val
    return tuple(lst)

  axis_size = a.shape[axis_int]
  arr_shape = replace(a.shape, 1)
  out_shape = lax.broadcast_shapes(idx_shape, arr_shape)
  if axis_size == 0:
    return lax.full(out_shape, 0, a.dtype)

  # Legacy behavior - should eventually be removed, since wrap_negative_indices
  # should be independent of indexing mode.
  if wrap_negative_indices is None:
    wrap_negative_indices = mode != "promise_in_bounds"

  index_dtype = lax_utils.index_dtype_for_axis_size(
      dtypes.dtype(indices), axis_size, wrap_negative_indices
  )
  indices = lax.convert_element_type(indices, index_dtype)

  if wrap_negative_indices:
    indices = _normalize_index(indices, axis_size)

  if mode == "one_hot":
    from jax import nn  # pyrefly: ignore[missing-import]

    hot = nn.one_hot(indices, axis_size, dtype=np.bool_)
    if a.ndim == 1:
      return einsum.einsum("...b,b->...", hot, a, preferred_element_type=a.dtype)
    if axis_int > len(string.ascii_letters) - 2:
      raise ValueError(
          "One Hot indexing is only supported for up to 50 leading dimensions."
      )
    labels = "".join([string.ascii_letters[i] for i in range(axis_int)])
    eq = labels + "y...z," + labels + "z...->" + labels + "y..."
    return einsum.einsum(
        eq,
        hot,
        a,
        precision=lax.Precision.HIGHEST,
        preferred_element_type=a.dtype,
    )

  index_dims = [i for i, idx in enumerate(idx_shape) if i == axis_int or not core.definitely_equal(idx, 1)]

  gather_index_shape = tuple(np.array(out_shape)[index_dims]) + (1,)
  gather_indices = lax.reshape(indices, gather_index_shape)
  slice_sizes = []
  offset_dims = []
  start_index_map = []
  collapsed_slice_dims = []
  operand_batching_dims = []
  start_indices_batching_dims = []

  # We will squeeze the array. i is the index of the unsqueezed shape, while
  # new_i is the index of the squeezed shape. j is the index of the gather
  # indices.
  dims_to_squeeze = []
  new_i = 0
  j = 0
  for i in range(rank):
    if i == axis_int:
      slice_sizes.append(1)
      start_index_map.append(new_i)
      collapsed_slice_dims.append(new_i)
      new_i += 1
      j += 1
    elif core.definitely_equal(idx_shape[i], 1):
      # If idx_shape[i] == 1, we can just take the entirety of the arr's axis
      # and avoid forming an iota index.
      offset_dims.append(i)
      slice_sizes.append(arr_shape[i])
      new_i += 1
    elif core.definitely_equal(arr_shape[i], 1):
      # If the array dimension is 1 but the index dimension is not, we will
      # squeeze this dimension.
      dims_to_squeeze.append(i)
      j += 1
    else:
      # Otherwise, idx_shape[i] == arr_shape[i]. Mark the dimensions in both
      # array and index as batching so corresponding elements are gathered.
      if core.definitely_equal(arr_shape[i], 0):
        slice_sizes.append(0)
      else:
        slice_sizes.append(1)
      operand_batching_dims.append(new_i)
      start_indices_batching_dims.append(j)
      new_i += 1
      j += 1

  # Squeeze a to remove singleton dimensions.
  a = lax.squeeze(a, dims_to_squeeze)
  dnums = slicing.GatherDimensionNumbers(
    offset_dims=tuple(offset_dims),
    collapsed_slice_dims=tuple(collapsed_slice_dims),
    start_index_map=tuple(start_index_map),
    operand_batching_dims=tuple(operand_batching_dims),
    start_indices_batching_dims=tuple(start_indices_batching_dims))
  return slicing.gather(a, gather_indices, dnums, tuple(slice_sizes),
                        mode="fill" if mode is None else mode, fill_value=fill_value)

