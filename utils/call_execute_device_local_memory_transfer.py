
def call_execute_device_local_memory_transfer(
    *,
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    src_allocation_key_as_array: jax.Array,
    src_transforms: tuple[Any, ...],
    dst_allocation_key_as_array: jax.Array,
    dst_transforms: tuple[Any, ...],
    barrier_allocation_key_as_array: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
):
  return callback.io_callback(
      functools.partial(
          _execute_device_local_memory_transfer, source_info=source_info
      ),
      TOKEN_SHAPE_DTYPE,
      token=token,
      device_id=device_id,
      grid_point_coords=grid_point_coords,
      thread_id=thread_id,
      src_allocation_key_as_array=src_allocation_key_as_array,
      src_transforms=src_transforms,
      dst_allocation_key_as_array=dst_allocation_key_as_array,
      dst_transforms=dst_transforms,
      barrier_allocation_key_as_array=barrier_allocation_key_as_array,
  )

