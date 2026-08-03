from typing import Set

def unique_processes_from_devices(device_array: np.ndarray) -> Set[int]:
  get_pids_from_devices = np.vectorize(process_index_from_device)
  return set(get_pids_from_devices(device_array).flat)

