
def _create_device_list(my_devices, my_device_maps, reverse_device_maps):
    if not my_devices:
        devices_set: set[torch.device] = set()
        for map_ in my_device_maps.values():
            devices_set.update(map_.keys())
        for map_ in reverse_device_maps.values():
            devices_set.update(map_.keys())
        devices_set.discard(torch.device("cpu"))
        my_devices = list(devices_set)
    my_devices = sorted(my_devices, key=lambda d: d.index)
    return my_devices


def _create_device_list(
    device_assignment: tuple[xc.Device, ...] | xc.DeviceList | None
    ) -> xc.DeviceList | None:
  if device_assignment is None or isinstance(device_assignment, xc.DeviceList):
    return device_assignment
  return _create_device_list_cached(device_assignment)

