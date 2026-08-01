
def _get_barrier_allocation_key_from_inval(
    inval, transforms_treedef, transforms_leaves
) -> jax.Array:
  # `inval` is expected to correspond to a barrier. Since we are interpreting,
  # `inval` will in fact contain the allocation key (which is a Jax array) for
  # the barrier.
  allocation_key_as_array = inval

  # Assert to check internal consistency: `allocation_key_as_array` should be
  # a 2-dim array (and the size of the first dimension equals the
  # `num_barriers` parameter from when the barrier was allocated).
  assert len(allocation_key_as_array.shape) == 2
  num_barriers = allocation_key_as_array.shape[0]

  index = _get_index_for_barrier_allocation_key(
      transforms_treedef, transforms_leaves
  )

  if index is None:
    if num_barriers != 1:
      raise ValueError(
          "Attempting to operate on barrier without indexing, but"
          f" `num_barriers = {num_barriers}`"
      )
    return allocation_key_as_array[0]
  else:
    return allocation_key_as_array[index]

