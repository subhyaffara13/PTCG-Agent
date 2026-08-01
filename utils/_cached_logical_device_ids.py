
def _cached_logical_device_ids(
    inp_device_list: xc.DeviceList,
    target_device_list: xc.DeviceList
) -> tuple[int, ...]:
  device_to_index = {d: i for i, d in enumerate(target_device_list)}
  return tuple(device_to_index[d] for d in inp_device_list)

