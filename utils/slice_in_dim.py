
def slice_in_dim(operand: Array | np.ndarray, start_index: int | None,
                 limit_index: int | None,
                 stride: int = 1, axis: int = 0) -> Array:
  """Convenience wrapper around :func:`lax.slice` applying to only one dimension.

  This is effectively equivalent to ``operand[..., start_index:limit_index:stride]``
  with the indexing applied on the specified axis.

  Args:
    operand: an array to slice.
    start_index: an optional start index (defaults to zero)
    limit_index: an optional end index (defaults to operand.shape[axis])
    stride: an optional stride (defaults to 1)
    axis: the axis along which to apply the slice (defaults to 0)

  Returns:
    An array containing the slice.

  Examples:
    Here is a one-dimensional example:

    >>> x = jnp.arange(4)
    >>> lax.slice_in_dim(x, 1, 3)
    Array([1, 2], dtype=int32)

    Here are some two-dimensional examples:

    >>> x = jnp.arange(12).reshape(4, 3)
    >>> x
    Array([[ 0,  1,  2],
           [ 3,  4,  5],
           [ 6,  7,  8],
           [ 9, 10, 11]], dtype=int32)

    >>> lax.slice_in_dim(x, 1, 3)
    Array([[3, 4, 5],
           [6, 7, 8]], dtype=int32)

    >>> lax.slice_in_dim(x, 1, 3, axis=1)
    Array([[ 1,  2],
           [ 4,  5],
           [ 7,  8],
           [10, 11]], dtype=int32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :func:`jax.lax.slice`
    - :func:`jax.lax.index_in_dim`
    - :func:`jax.lax.dynamic_slice_in_dim`
  """
  start_indices = [0] * operand.ndim
  limit_indices = list(operand.shape)
  strides = [1] * operand.ndim

  # translate `None`
  len_axis = operand.shape[axis]
  start_index_int = (core._canonicalize_dimension(start_index)
                     if start_index is not None else 0)
  limit_index_int = (core._canonicalize_dimension(limit_index)
                     if limit_index is not None else len_axis)

  # translate negative indices
  if start_index_int < 0:
    start_index_int = start_index_int + len_axis
  if limit_index_int < 0:
    limit_index_int = limit_index_int + len_axis

  axis = int(axis)
  start_indices[axis] = start_index_int
  limit_indices[axis] = limit_index_int
  strides[axis] = core._canonicalize_dimension(stride)

  return slice(operand, start_indices, limit_indices, strides)

