
def _get_devices_properties(device_ids):
    # all device properties
    return [_get_device_attr(lambda m: m.get_device_properties(i)) for i in device_ids]

