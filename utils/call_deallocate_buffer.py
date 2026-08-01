
def call_deallocate_buffer(
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    allocation_key_as_array: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
):
  return callback.io_callback(
      functools.partial(_deallocate_buffer, source_info=source_info),
      TOKEN_SHAPE_DTYPE,
      token,
      device_id,
      grid_point_coords,
      thread_id,
      allocation_key_as_array,
  )

