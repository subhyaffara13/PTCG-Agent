
def _deallocate_barrier(
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
  del device_id, grid_point_coords, thread_id

  assert len(allocation_key_as_array.shape) == 2
  num_barriers = allocation_key_as_array.shape[0]

  keys_to_deallocate = []
  for i in range(num_barriers):
    keys_to_deallocate.append(allocation_key_as_array[i, :])

  shared_memory = _get_shared_memory()

  for key in keys_to_deallocate:
    barrier_allocation_key = HostAllocationKey.from_array(key)
    shared_memory.deallocate_barrier(
        barrier_allocation_key,
        logging_info=interpret_utils.GPULoggingInfo(
            device_id=device_id_as_int,
            grid_point_coords=grid_point_coords_as_tuple,
            thread_id=thread_id_as_int,
            source_info=source_info,
        ),
    )
  return token

