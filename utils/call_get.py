
def call_get(
    *,
    token: jax.Array,
    result_shape_and_dtype,
    device_id: jax.Array,
    grid_point_coords: jax.Array | None,
    thread_id: jax.Array,
    allocation_key_as_array: jax.Array,
    transforms,
    block_indices=None,
    grid_loop_idx=None,
    clock=None,
    source_info=None,
    input_name=None,
) -> tuple[jax.Array, jax.Array]:
  return callback.io_callback(
      functools.partial(_get, source_info=source_info, input_name=input_name),
      (TOKEN_SHAPE_DTYPE, result_shape_and_dtype),
      token,
      device_id,
      grid_point_coords,
      thread_id,
      allocation_key_as_array,
      transforms,
      block_indices,
      grid_loop_idx,
      clock,
  )

