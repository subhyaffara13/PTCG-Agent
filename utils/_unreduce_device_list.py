import functools

def _unreduce_device_list(device_ids: Sequence[int]) -> DeviceList:
  cpu_device_map = _get_cpu_device_map()
  devices = np.vectorize(functools.partial(_lookup_cpu_device, cpu_device_map))(
      device_ids)
  return DeviceList(tuple(devices))

