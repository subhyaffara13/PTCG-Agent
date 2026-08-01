
def _allocate_barriers(
    *,
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    axes_dims: tuple[int, ...],
    num_arrivals: jax.Array,
    num_barriers: jax.Array,
    ref_count: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
) -> tuple[jax.Array, jax.Array]:
  device_id_as_int = int(device_id)
  grid_point_coords_as_tuple = tuple(int(x) for x in grid_point_coords)
  thread_id_as_int = int(thread_id)
  axes_dims = tuple(int(x) for x in axes_dims)
  num_arrivals_as_int = int(num_arrivals)
  num_barriers_as_int = int(num_barriers)
  ref_count_as_int = int(ref_count)
  del device_id, grid_point_coords, thread_id, num_arrivals, num_barriers, ref_count

  shared_memory = _get_shared_memory()

  keys = []
  for _ in range(num_barriers_as_int):
    # Advance `shared_memory`'s internal buffer id counter for all threads that
    # call into this function.
    barrier_id = shared_memory.get_next_buffer_id(
        device_id_as_int, thread_id_as_int
    )
    smem_space_id = IDX_BY_GPU_MEMORY_SPACE[mosaic_gpu_core.SMEM]

    # Barriers are shared between threads. For each group of threads that share
    # a barrier, we compute the thread ID to be used for the allocation key.
    # Invariant: `thread_id_for_key` is the same for all threads in a group that
    # shares the barrier.
    thread_id_for_key = get_thread_id_for_collective_allocation_key(
        thread_id_as_int, axes_dims, is_last_thread_axis_collective=True
    )

    key = HostAllocationKey(
        memory_space_id=smem_space_id,
        device_id=device_id_as_int,
        thread_id=thread_id_for_key,
        initial_ref_count=ref_count_as_int,
        buffer_id=barrier_id,
    )

    shared_memory.allocate_barrier(
        key,
        ref_count=ref_count_as_int,
        num_arrivals=num_arrivals_as_int,
        logging_info=interpret_utils.GPULoggingInfo(
            device_id=device_id_as_int,
            grid_point_coords=grid_point_coords_as_tuple,
            thread_id=thread_id_as_int,
            source_info=source_info,
        ),
    )
    keys.append(key.as_jax_array)

  assert len(keys) == num_barriers_as_int
  return token, jnp.array(keys, dtype=np.int32)

