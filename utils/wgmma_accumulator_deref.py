
def wgmma_accumulator_deref(
    *,
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    acc_allocation_key_as_array: jax.Array,
    wait_n: int | None,
    source_info: source_info_util.SourceInfo | None = None,
):
  # TODO(jburnim): wait_n for async wgmma.
  del wait_n

  device_id: int = int(device_id)  # pyrefly: ignore[redefinition]
  grid_point_coords: tuple[int, ...] = tuple(int(x) for x in grid_point_coords)  # pyrefly: ignore[redefinition]
  thread_id: int = int(thread_id)  # pyrefly: ignore[redefinition]
  acc_allocation_key = HostAllocationKey.from_array(acc_allocation_key_as_array)

  shared_memory = _get_shared_memory()
  global_thread_id = shared_memory.get_global_thread_id(device_id, thread_id)

  logging_info = interpret_utils.GPULoggingInfo(
      device_id=device_id,
      grid_point_coords=grid_point_coords,
      thread_id=0,
      source_info=source_info,
  )

  acc, _, _ = shared_memory.get_buffer_content(
      acc_allocation_key, (), global_thread_id, logging_info=logging_info)
  return token, acc

