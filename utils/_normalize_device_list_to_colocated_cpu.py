
def _normalize_device_list_to_colocated_cpu(
    device_list: cp_serialization.DeviceList,
) -> cp_serialization.DeviceList:
  if all(_device_platform(device) == 'cpu' for device in device_list):
    return device_list
  return cp_serialization.DeviceList(
      tuple(_to_serializable_cpu_device(device) for device in device_list)
  )

