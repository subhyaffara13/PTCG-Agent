
def call_allocate_buffer(
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    allocation_request_as_array: jax.Array,
    value: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
) -> tuple[jax.Array, jax.Array]:
  return callback.io_callback(
      functools.partial(_allocate_buffer, source_info=source_info),
      (TOKEN_SHAPE_DTYPE, HostAllocationKey.shape_and_dtype()),
      token,
      device_id,
      grid_point_coords,
      thread_id,
      allocation_request_as_array,
      value,
  )

