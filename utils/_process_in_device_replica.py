
def _process_in_device_replica(
    process_index: int, device_slice: np.ndarray
) -> bool:
  return process_index in multihost.unique_processes_from_devices(device_slice)

