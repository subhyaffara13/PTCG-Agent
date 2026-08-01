
def dynamic_update_slice_in_dim(operand: Array | np.ndarray,
                                update: ArrayLike,
                                start_index: ArrayLike, axis: int,
                                *,
                                allow_negative_indices: bool = True) -> Array:
  """Convenience wrapper around :func:`dynamic_update_slice` to update
  a slice in a single ``axis``.

  Args:
    operand: an array to slice.
    update: an array containing the new values to write onto `operand`.
    start_index: a single scalar index
    axis: the axis of the update.
    allow_negative_indices: boolean specifying whether negative indices are
      allowed. If true, negative indices are taken relative to the end of the
      array. If false, negative indices are out of bounds and the result is
      implementation defined.

  Returns:
    The updated array

  Examples:

    >>> x = jnp.zeros(6)
    >>> y = jnp.ones(3)
    >>> dynamic_update_slice_in_dim(x, y, 2, axis=0)
    Array([0., 0., 1., 1., 1., 0.], dtype=float32)

    If the update slice is too large to fit in the array, the start
    index will be adjusted to make it fit:

    >>> dynamic_update_slice_in_dim(x, y, 3, axis=0)
    Array([0., 0., 0., 1., 1., 1.], dtype=float32)
    >>> dynamic_update_slice_in_dim(x, y, 5, axis=0)
    Array([0., 0., 0., 1., 1., 1.], dtype=float32)

    Here is an example of a two-dimensional slice update:

    >>> x = jnp.zeros((4, 4))
    >>> y = jnp.ones((2, 4))
    >>> dynamic_update_slice_in_dim(x, y, 1, axis=0)
    Array([[0., 0., 0., 0.],
           [1., 1., 1., 1.],
           [1., 1., 1., 1.],
           [0., 0., 0., 0.]], dtype=float32)

    Note that the shape of the additional axes in ``update`` need not
    match the associated dimensions of the ``operand``:

    >>> y = jnp.ones((2, 3))
    >>> dynamic_update_slice_in_dim(x, y, 1, axis=0)
    Array([[0., 0., 0., 0.],
           [1., 1., 1., 0.],
           [1., 1., 1., 0.],
           [0., 0., 0., 0.]], dtype=float32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :func:`jax.lax.dynamic_update_slice`
    - :func:`jax.lax.dynamic_update_index_in_dim`
    - :func:`jax.lax.dynamic_slice_in_dim`
  """
  axis = int(axis)
  start_indices: list[ArrayLike] = [lax._const(start_index, 0)] * lax._ndim(operand)
  start_indices[axis] = start_index
  allow_negative = [False] * operand.ndim
  allow_negative[axis] = allow_negative_indices
  return dynamic_update_slice(operand, update, start_indices,
                              allow_negative_indices=allow_negative)

