
def _initialize_shared_memory(
    *,
    token: jax.Array,
    num_gpus: jax.Array,
    num_threads_per_block: jax.Array,
    num_blocks_per_cluster: jax.Array,
    interpret_params: InterpretGPUParams,
):
  global _shared_memory, _races

  num_gpus_as_int = int(num_gpus)
  num_threads_per_block_as_int = int(num_threads_per_block)
  num_blocks_per_cluster_as_int = int(num_blocks_per_cluster)
  del num_gpus, num_threads_per_block, num_blocks_per_cluster

  num_total_concurrent_threads = (
      num_gpus_as_int
      * num_threads_per_block_as_int
      * num_blocks_per_cluster_as_int
  )

  with _shared_memory_init_lock:
    if _shared_memory is None:
      _races = RaceDetectionState(num_cores=num_total_concurrent_threads)
      _shared_memory = memory.GPUSharedMemory(
          num_devices=num_gpus_as_int,
          num_threads_per_block=num_threads_per_block_as_int,
          num_blocks_per_cluster=num_blocks_per_cluster_as_int,
          num_tma_threads_per_device=interpret_params.num_tma_threads_per_device,
          out_of_bounds_reads=interpret_params.out_of_bounds_reads,
          # TODO(nrink): Support different DMA execution modes on GPU.
          dma_execution_mode="eager",
          uninitialized_memory=interpret_params.uninitialized_memory,
          detect_races=interpret_params.detect_races,
          barrier=threading.Barrier(num_gpus_as_int, action=lambda: None),
          clean_up_barrier=threading.Barrier(
              num_gpus_as_int, action=_clear_shared_memory
          ),
          logging_mode=interpret_params.logging_mode,
      )
  # The naming of the `num_cores` property of `SharedMemory` originates from the
  # support for multipl cores in a (Megacore) TPU device. As commented above, on
  # GPU we model multiple Pallas threads per device as _cores_ in the
  # (TPU-/Megacore-)inspired terminology of `SharedMemory`.
  assert _shared_memory.num_cores == num_total_concurrent_threads
  return token


def _initialize_shared_memory(
    token, device_id, num_devices, num_cores_per_device, *, interpret_params
):
  global _shared_memory, races, dma_id_counter
  del device_id

  num_devices = int(num_devices)
  num_cores_per_device = int(num_cores_per_device)
  num_cores = num_devices * num_cores_per_device

  with _shared_memory_init_lock:
    if _shared_memory is None:
      vector_clock_size = interpret_params.get_vector_clock_size(num_devices)
      races = RaceDetectionState(num_cores=num_cores)
      dma_id_counter = interpret_utils.Counter(100)
      _shared_memory = memory.SharedMemory(
          num_devices=num_devices,
          num_cores_per_device=num_cores_per_device,
          out_of_bounds_reads=interpret_params.out_of_bounds_reads,
          buffer_bounds=interpret_params.buffer_bounds,
          dma_execution_mode=interpret_params.dma_execution_mode,
          uninitialized_memory=interpret_params.uninitialized_memory,
          detect_races=interpret_params.detect_races,
          vector_clock_size=vector_clock_size,
          clocks=[
              vc.make_vector_clock(vector_clock_size) for _ in range(num_cores)
          ],
          barrier=threading.Barrier(
              num_devices, action=_update_clocks_for_global_barrier
          ),
          clean_up_barrier=threading.Barrier(
              num_devices, action=_clear_shared_memory
          ),
          logging_mode=interpret_params.logging_mode,
      )
  assert _shared_memory.num_cores == num_cores
  return token

