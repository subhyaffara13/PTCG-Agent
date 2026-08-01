
def _deallocate_buffer(
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    allocation_key_as_array: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
):
  """Decreases the reference count of the buffer with `allocation_key` (Deallocates the buffer if its reference count becomes zero)."""
  device_id_as_int = int(device_id)
  grid_point_coords_as_tuple = tuple(int(x) for x in grid_point_coords)
  thread_id_as_int = int(thread_id)
  allocation_key = HostAllocationKey.from_array(allocation_key_as_array)
  del device_id, grid_point_coords, thread_id, allocation_key_as_array
  shared_memory = _get_shared_memory()

  shared_memory.deallocate_buffer(
      allocation_key,
      logging_info=interpret_utils.GPULoggingInfo(
          device_id=device_id_as_int,
          grid_point_coords=grid_point_coords_as_tuple,
          thread_id=thread_id_as_int,
          source_info=source_info,
      ),
  )
  return token


def _deallocate_buffer(
    token, device_id, local_core_id, memory_space, buffer_id, source_info=None
):
  device_id = int(device_id)
  local_core_id = int(local_core_id)
  memory_space = TPU_MEMORY_SPACE_NAMES[int(memory_space)]
  buffer_id = int(buffer_id)

  local_core_id = _local_core_id_or_zero_if_hbm(local_core_id, memory_space)

  shared_memory = _get_shared_memory()
  key = (memory_space, buffer_id, device_id, local_core_id)
  shared_memory.deallocate_buffer(
      key,
      logging_info=interpret_utils.TPULoggingInfo(
          device_id=device_id,
          local_core_id=local_core_id,
          source_info=source_info,
      ),
  )
  return token

