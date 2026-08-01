
def _allocate_buffer(
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    allocation_request_as_array: jax.Array,
    value: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
) -> tuple[jax.Array, jax.Array]:
  """Allocates a buffer for the given `allocation_request`.

  Args:
    allocation_reques_as_array: Array that converts into a
      `HostAllocationRequest`.
    value: Array of values to initialize the allocated buffer with.
    source_info: Information about the source code location of the allocation.

  Returns:
    `AllocationKey` to refer to the allocated buffer.
  """
  device_id_as_int = int(device_id)
  grid_point_coords_as_tuple = tuple(int(x) for x in grid_point_coords)
  thread_id_as_int = int(thread_id)
  allocation_request = HostAllocationRequest.from_array(
      allocation_request_as_array
  )
  del device_id, grid_point_coords, thread_id, allocation_request_as_array

  shared_memory = _get_shared_memory()

  if (allocation_request.memory_space_id
      == get_memory_space_idx(mosaic_gpu_core.MemorySpace.REGS)):
    # For barrier and buffer identifiers to line up across threads, we rely on
    # each thread making the same sequence of allocations.  But threads are
    # permitted to make different REGS allocations, so we use a different
    # sequence of integer identifiers for REGS allocations.
    buffer_id = shared_memory.get_next_wgmma_accumulator_id(
        device_id_as_int, thread_id_as_int)
  else:
    buffer_id = shared_memory.get_next_buffer_id(
        device_id_as_int, thread_id_as_int)

  key = HostAllocationKey(
      memory_space_id=allocation_request.memory_space_id,
      device_id=allocation_request.device_id,
      thread_id=allocation_request.thread_id,
      initial_ref_count=allocation_request.initial_ref_count,
      buffer_id=buffer_id,
  )
  ref_count = allocation_request.initial_ref_count
  shared_memory.allocate_buffer(
      key,
      ref_count=ref_count,
      value=np.array(value),
      logging_info=interpret_utils.GPULoggingInfo(
          device_id=device_id_as_int,
          grid_point_coords=grid_point_coords_as_tuple,
          thread_id=thread_id_as_int,
          source_info=source_info,
      ),
  )
  return token, key.as_jax_array


def _allocate_buffer(
    token: Array,
    device_id: Array,
    local_core_id: Array | None,
    memory_space: Array,
    val: Array,
    source_info: source_info_util.SourceInfo | None = None,
):
  """Allocates a memory buffer on the device with id `device_id` and core with id `local_core_id`.

  Args:
    device_id: Singleton array holding the device id where the buffer will be
      allocated.
    local_core_id: None or singleton array holding the core id where the buffer
      will be allocated. If None, a buffer will be allocated on each cores on
      the device.
    memory_space: Singleton array indicating the memory space to allocate the
      buffer in. If the corresponding memory space is "any" (i.e. HBM), at most
      one buffer will be allocated and it will belong to (local) core id 0.
    val: Array of values to initialize the allocated buffer with.
    source_info: Information about the source code location of the allocation.

  Returns:
    Integer id for the allocated buffer.
  """
  device_id: int = int(device_id)  # pyrefly: ignore[redefinition]
  memory_space_str = TPU_MEMORY_SPACE_NAMES[int(memory_space)]
  value = np.array(val)
  del memory_space, val

  shared_memory = _get_shared_memory()

  logical_shape = value.shape
  if (
      shared_memory.buffer_bounds == 'padded'
      and memory_space_str != mosaic_core.MemorySpace.SMEM.value
  ):
    value = _get_with_padding(value, shared_memory.uninitialized_memory)

  if local_core_id is None:
    local_core_id_int = 0
    local_core_ids = tuple(range(shared_memory.num_cores_per_device))
  else:
    local_core_id_int = int(local_core_id)
    local_core_ids = (local_core_id_int,)
  del local_core_id

  local_core_id_to_buffer_id: dict[int, int] = {}
  for lci in local_core_ids:
    buffer_id = shared_memory.get_next_buffer_id(device_id, lci)
    if memory_space_str in ['any', 'hbm']:
      # If allocating in HBM, only actually allocate a buffer once. The first
      # local core (i.e. thread) that gets here allocates the buffer, but the
      # buffer is still keyed in the shared memory with core ID 0. However,
      # since the buffer is shared across all cores, we initialize the buffer's
      # `ref_count` with the number of cores per device. This ensures that the
      # buffer is not deallocated until all cores have exited the scope of the
      # allocation (e.g. have exited the body of a `run_scoped`).
      key = (memory_space_str, buffer_id, device_id, 0)
      ref_count = shared_memory.num_cores_per_device
    else:
      key = (memory_space_str, buffer_id, device_id, lci)
      ref_count = 1
      if len(local_core_id_to_buffer_id) > 0:
        # If we are allocating more than one buffer, we must make additional
        # copies of `val` so that each buffer is a distinct ndarray.
        value = value.copy()

    shared_memory.allocate_buffer(
        key,
        ref_count=ref_count,
        value=value,
        logical_shape=logical_shape,
        logging_info=interpret_utils.TPULoggingInfo(
            device_id=device_id,
            local_core_id=lci,
            source_info=source_info,
        ),
    )
    local_core_id_to_buffer_id[lci] = buffer_id

  # The buffer ids should always be kept in sync across all cores.
  assert all(
      buffer_id == local_core_id_to_buffer_id[local_core_id_int]
      for buffer_id in local_core_id_to_buffer_id.values()
  )
  # TODO(jburnim): Raise an error if buffer_id is too big for int16.
  return token, np.int16(local_core_id_to_buffer_id[local_core_id_int])

