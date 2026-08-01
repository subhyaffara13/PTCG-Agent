
def _min_results_across_devices(kernels_ms : list[tuple[str, float]]) -> float:
  # We choose the minimum across processes to choose the runtime that didn't
  # include devices waiting for other devices.
  if is_nvshmem_used():
    time_us = sum(t * 1e3 for _, t in kernels_ms)
    return min(multihost_utils.process_allgather(time_us).tolist())

  # profiler.measures measures all devices visible to the process, so we
  # need to select the mimimum result of each kernel across devices.
  # This code relies on the fact that with collective metadata a single kernel
  # with unique name is launched on each device.
  min_values : dict[str, float] = {}
  for kernel_name, t in kernels_ms:
    if kernel_name not in min_values or t < min_values[kernel_name]:
      min_values[kernel_name] = t
  return sum(time_ms * 1e3 for time_ms in min_values.values())

