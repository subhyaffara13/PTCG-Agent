
def index_in_dim(operand: Array | np.ndarray, index: int, axis: int = 0,
                 keepdims: bool = True) -> Array:
  """Convenience wrapper around :func:`lax.slice` to perform int indexing.

  This is effectively equivalent to ``operand[..., index]``
  with the indexing applied on the specified axis.

  Args:
    operand: an array to index.
    index: integer index
    axis: the axis along which to apply the index (defaults to 0)
    keepdims: boolean specifying whether the output array should preserve the
      rank of the input (default=True)

  Returns:
    The subarray at the specified index.

  Examples:
    Here is a one-dimensional example:

    >>> x = jnp.arange(4)
    >>> lax.index_in_dim(x, 2)
    Array([2], dtype=int32)

    >>> lax.index_in_dim(x, 2, keepdims=False)
    Array(2, dtype=int32)

    Here are some two-dimensional examples:

    >>> x = jnp.arange(12).reshape(3, 4)
    >>> x
    Array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]], dtype=int32)

    >>> lax.index_in_dim(x, 1)
    Array([[4, 5, 6, 7]], dtype=int32)

    >>> lax.index_in_dim(x, 1, axis=1, keepdims=False)
    Array([1, 5, 9], dtype=int32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :func:`jax.lax.slice`
    - :func:`jax.lax.slice_in_dim`
    - :func:`jax.lax.dynamic_index_in_dim`
  """
  index, axis = core._canonicalize_dimension(index), int(axis)
  axis_size = operand.shape[axis]
  wrapped_index = index + axis_size if index < 0 else index
  if not 0 <= wrapped_index < axis_size:
    msg = 'index {} is out of bounds for axis {} with size {}'
    raise IndexError(msg.format(index, axis, axis_size))
  result = slice_in_dim(operand, wrapped_index, wrapped_index + 1, 1, axis)
  if keepdims:
    return result
  else:
    return lax.squeeze(result, (axis,))

