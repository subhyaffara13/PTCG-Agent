
def register_device_op_overrides(
    device: str, device_op_overrides: DeviceOpOverrides
) -> None:
    device_op_overrides_dict[device] = device_op_overrides

