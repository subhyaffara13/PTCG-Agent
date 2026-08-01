
def get_device_op_overrides(device: str) -> DeviceOpOverrides:
    assert isinstance(device, str), type(device)
    _initialize_device_op_overrides()
    return device_op_overrides_dict[device]

