
def _streaming_stack(
    items: Sequence[jax.Array],
    axis: int,
    sharding: jax.sharding.Sharding | None = None,
) -> jax.Array:
  """Stacks items along a given axis.

  Memory optimized code path for stacking arrays when the source arrays are in
  host memory and the target array sharding is in device memory.

  Args:
    items: Sequence of arrays to stack.
    axis: Axis along which to stack.
    sharding: Optional target sharding for the stacked array.

  Returns:
    The stacked array.
  """
  num_arrays = len(items)
  base_shape = items[0].shape

  # Calculate the final shape, for example with 256 arrays of shape (32, 1024):
  # base=(32, 1024), axis=1 -> final=(32, 256, 1024)
  final_shape = list(base_shape)
  final_shape.insert(axis, num_arrays)
  final_shape = tuple(final_shape)

  def _callback(indices):
    # Extract the slice for the stacking axis
    stack_slice = indices[axis]
    start, stop, _ = stack_slice.indices(num_arrays)
    # Grab the requested chunk of arrays from the host list
    chunk_list = items[start:stop]
    # Stack them locally on the CPU along the correct axis
    stacked_chunk = jnp.stack(chunk_list, axis=axis)
    return stacked_chunk

  return jax.make_array_from_callback(tuple(final_shape), sharding, _callback)

