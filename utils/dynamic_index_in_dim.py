
def dynamic_index_in_dim(operand: Array | np.ndarray,
                         index: ArrayLike,
                         axis: int = 0, keepdims: bool = True,
                         *,
                         allow_negative_indices: bool = True) -> Array:
  """Convenience wrapper around dynamic_slice to perform int indexing.

  This is roughly equivalent to the following Python indexing syntax applied
  along the specified axis: ``operand[..., index]``.

  Args:
    operand: an array to slice.
    index: the (possibly dynamic) start index
    axis: the axis along which to apply the slice (defaults to 0)
    keepdims: boolean specifying whether the output should have the same rank as
      the input (default = True)
    allow_negative_indices: boolean specifying whether negative indices are
      allowed. If true, negative indices are taken relative to the end of the
      array. If false, negative indices are out of bounds and the result is
      implementation defined.

  Returns:
    An array containing the slice.

  Examples:
    Here is a one-dimensional example:

    >>> x = jnp.arange(5)
    >>> dynamic_index_in_dim(x, 1)
    Array([1], dtype=int32)

    >>> dynamic_index_in_dim(x, 1, keepdims=False)
    Array(1, dtype=int32)

    Here is a two-dimensional example:

    >>> x = jnp.arange(12).reshape(3, 4)
    >>> x
    Array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]], dtype=int32)

    >>> dynamic_index_in_dim(x, 1, axis=1, keepdims=False)
    Array([1, 5, 9], dtype=int32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :func:`jax.lax.index_in_dim`
    - :func:`jax.lax.dynamic_slice`
    - :func:`jax.lax.dynamic_slice_in_dim`
  """
  result = dynamic_slice_in_dim(operand, index, 1, axis,
                                allow_negative_indices=allow_negative_indices)
  if keepdims:
    return result
  else:
    return lax.squeeze(result, (axis,))

