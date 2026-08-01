
def dynamic_update_index_in_dim(operand: Array | np.ndarray,
                                update: ArrayLike, index: ArrayLike,
                                axis: int, *,
                                allow_negative_indices: bool = True) -> Array:
  """Convenience wrapper around :func:`dynamic_update_slice` to update a slice
  of size 1 in a single ``axis``.

  Args:
    operand: an array to slice.
    update: an array containing the new values to write onto `operand`.
    index: a single scalar index
    axis: the axis of the update.
    allow_negative_indices: boolean specifying whether negative indices are
      allowed. If true, negative indices are taken relative to the end of the
      array. If false, negative indices are out of bounds and the result is
      implementation defined.

  Returns:
    The updated array

  Examples:

    >>> x = jnp.zeros(6)
    >>> y = 1.0
    >>> dynamic_update_index_in_dim(x, y, 2, axis=0)
    Array([0., 0., 1., 0., 0., 0.], dtype=float32)

    >>> y = jnp.array([1.0])
    >>> dynamic_update_index_in_dim(x, y, 2, axis=0)
    Array([0., 0., 1., 0., 0., 0.], dtype=float32)

    If the specified index is out of bounds, the index will be clipped to the
    valid range:

    >>> dynamic_update_index_in_dim(x, y, 10, axis=0)
    Array([0., 0., 0., 0., 0., 1.], dtype=float32)

    Here is an example of a two-dimensional dynamic index update:

    >>> x = jnp.zeros((4, 4))
    >>> y = jnp.ones(4)
    >>> dynamic_update_index_in_dim(x, y, 1, axis=0)
    Array([[0., 0., 0., 0.],
          [1., 1., 1., 1.],
          [0., 0., 0., 0.],
          [0., 0., 0., 0.]], dtype=float32)

    Note that the shape of the additional axes in ``update`` need not
    match the associated dimensions of the ``operand``:

    >>> y = jnp.ones((1, 3))
    >>> dynamic_update_index_in_dim(x, y, 1, 0)
    Array([[0., 0., 0., 0.],
           [1., 1., 1., 0.],
           [0., 0., 0., 0.],
           [0., 0., 0., 0.]], dtype=float32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :func:`jax.lax.dynamic_update_slice`
    - :func:`jax.lax.dynamic_update_index_in_dim`
    - :func:`jax.lax.dynamic_index_in_dim`
  """
  axis = int(axis)
  if lax._ndim(update) != lax._ndim(operand):
    assert lax._ndim(update) + 1 == lax._ndim(operand)
    update = lax.expand_dims(update, (axis,))
  return dynamic_update_slice_in_dim(
      operand, update, index, axis,
      allow_negative_indices=allow_negative_indices)

