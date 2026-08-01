
def dynamic_slice_in_dim(operand: Array | np.ndarray,
                         start_index: ArrayLike,
                         slice_size: int, axis: int = 0, *,
                         allow_negative_indices: bool = True) -> Array:
  """Convenience wrapper around :func:`lax.dynamic_slice` applied to one dimension.

  This is roughly equivalent to the following Python indexing syntax applied
  along the specified axis: ``operand[..., start_index:start_index + slice_size]``.

  Args:
    operand: an array to slice.
    start_index: the (possibly dynamic) start index
    slice_size: the static slice size
    axis: the axis along which to apply the slice (defaults to 0)
    allow_negative_indices: boolean specifying whether negative indices are
      allowed. If true, negative indices are taken relative to the end of the
      array. If false, negative indices are out of bounds and the result is
      implementation defined.

  Returns:
    An array containing the slice.

  Examples:
    Here is a one-dimensional example:

    >>> x = jnp.arange(5)
    >>> dynamic_slice_in_dim(x, 1, 3)
    Array([1, 2, 3], dtype=int32)

    Like `jax.lax.dynamic_slice`, out-of-bound slices will be clipped to the
    valid range:

    >>> dynamic_slice_in_dim(x, 4, 3)
    Array([2, 3, 4], dtype=int32)

    Here is a two-dimensional example:

    >>> x = jnp.arange(12).reshape(3, 4)
    >>> x
    Array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]], dtype=int32)

    >>> dynamic_slice_in_dim(x, 1, 2, axis=1)
    Array([[ 1,  2],
           [ 5,  6],
           [ 9, 10]], dtype=int32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :func:`jax.lax.slice_in_dim`
    - :func:`jax.lax.dynamic_slice`
    - :func:`jax.lax.dynamic_index_in_dim`
  """
  start_indices: list[ArrayLike] = [lax._const(start_index, 0)] * operand.ndim
  slice_sizes = list(operand.shape)
  axis = int(axis)
  allow_negative = [False] * operand.ndim
  allow_negative[axis] = allow_negative_indices
  start_indices[axis] = start_index
  slice_sizes[axis] = core._canonicalize_dimension(slice_size)
  return dynamic_slice(operand, start_indices, slice_sizes,
                       allow_negative_indices=allow_negative)

