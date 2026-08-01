
def process_index_from_device_id(device_id: int) -> int:
  """Get process index from device id."""
  if jax.devices()[0].platform == 'gpu':
    return device_id // jax.local_device_count()
  elif jax.devices()[0].platform == 'tpu':
    if hasattr(jax.devices()[0], 'slice_index'):
      # Note that it is possible for single slice TPU devices to have  a slice
      # index.
      num_slices = max([d.slice_index for d in jax.devices()]) + 1
      # Multi-slice TPU workload.
      if num_slices > 1:
        num_processes_per_slice = jax.process_count() // num_slices
        # This is based on how Megascale device ids are assigned.
        # See platforms/xla/megascale/common/multi_slice_topology.h.
        slice_id = device_id // 100000 - 1
        local_process_id = device_id % 100000 // jax.local_device_count()
        return slice_id * num_processes_per_slice + local_process_id
    # Single slice TPU workload.
    return device_id // jax.local_device_count()
  # CPU workload.
  else:
    # This is based on how CPU device ids are assigned.
    # See tensorflow/compiler/xla/pjrt/cpu/cpu_topology.h.
    return device_id // (1 << 17) // jax.local_device_count()

