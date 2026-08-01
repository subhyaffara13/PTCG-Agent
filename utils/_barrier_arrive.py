
def _barrier_arrive(
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    allocation_key_as_array: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
):
  device_id_as_int = int(device_id)
  grid_point_coords_as_tuple = tuple(int(x) for x in grid_point_coords)
  thread_id_as_int = int(thread_id)
  barrier_key = HostAllocationKey.from_array(allocation_key_as_array)
  del device_id, grid_point_coords, thread_id, allocation_key_as_array

  shared_memory = _get_shared_memory()

  barrier, clock = shared_memory.get_barrier_and_increment_clock(
      barrier_key, device_id_as_int, thread_id_as_int
  )
  barrier.arrive(
      clock,
      logging_info=interpret_utils.GPULoggingInfo(
          device_id=device_id_as_int,
          grid_point_coords=grid_point_coords_as_tuple,
          thread_id=thread_id_as_int,
          source_info=source_info,
      ),
  )
  return token

