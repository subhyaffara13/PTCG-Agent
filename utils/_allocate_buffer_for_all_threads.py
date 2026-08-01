
def _allocate_buffer_for_all_threads(
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array | None,
    allocation_request_as_array: jax.Array,
    value: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
) -> tuple[jax.Array, jax.Array]:
  """Allocates a buffer for the given `allocation_request`.

  While only a single buffer is allocated, we increment the next buffer ID on
  `_shared_memory` for all threads. (This is analogous to the behavior when
  interpreting TPU kernels with multiple cores per TPU device.)

  Args:
    allocation_request_as_array: Array that converts into an
      `HostAllocationRequest` with `thread_id` set to zero. This requirement can
      be thought of as associating the allocated buffer (that is shared across
      all threads) with the zeroth thread.
    value: Array of values to initialize the allocated buffer with.

  Returns:
    `AllocationKey` to refer to the allocated buffer.

  Raises:
    ValueError: If the `thread_id` in `allocation_request` is not zero.
  """
  device_id_as_int = int(device_id)
  grid_point_coords_as_tuple = (
      tuple(int(x) for x in grid_point_coords)
      if grid_point_coords is not None
      else None
  )
  allocation_request = HostAllocationRequest.from_array(
      allocation_request_as_array
  )
  del device_id, grid_point_coords, allocation_request_as_array

  if allocation_request.thread_id != 0:
    raise ValueError(
        "`thread_id` must be zero when allocating a buffer for all threads"
    )
  assert allocation_request.memory_space_id != get_memory_space_idx(
      mosaic_gpu_core.MemorySpace.REGS
  )

  shared_memory = _get_shared_memory()

  key: HostAllocationKey | None = None
  buffer_id: int | None = None
  for thread_id in range(shared_memory.num_cores_per_device):
    buffer_id_for_thread_id = shared_memory.get_next_buffer_id(
        device_id_as_int, thread_id
    )
    if not buffer_id:
      buffer_id = buffer_id_for_thread_id
    else:
      # We keep the buffer ids in sync across all threads. This implies, in
      # particular, that every instance of the assignment to `key` below assigns
      # an `AllocationKey` object with the same attributes.
      assert buffer_id == buffer_id_for_thread_id

    key = HostAllocationKey(
        memory_space_id=allocation_request.memory_space_id,
        device_id=allocation_request.device_id,
        thread_id=0,
        initial_ref_count=allocation_request.initial_ref_count,
        buffer_id=buffer_id,
    )
    ref_count = allocation_request.initial_ref_count
    # We rely on the fact that `allocate_buffer` will not allocate a new buffer
    # if one with the same key already exists.
    shared_memory.allocate_buffer(
        key,
        ref_count=ref_count,
        value=np.array(value),
        logging_info=interpret_utils.GPULoggingInfo(
            device_id=device_id_as_int,
            grid_point_coords=grid_point_coords_as_tuple,
            thread_id=0,
            source_info=source_info,
        ),
    )

  # We expect the `for`-loop above to have executed its body at least once.
  assert key is not None
  return token, key.as_jax_array

