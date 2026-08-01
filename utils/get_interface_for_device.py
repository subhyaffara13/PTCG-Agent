
def get_interface_for_device(device: str | torch.device) -> type[DeviceInterface]:
    if isinstance(device, torch.device):
        device = device.type
    if not _device_initialized:
        init_device_reg()
    if device in device_interfaces:
        return device_interfaces[device]
    raise NotImplementedError(f"No interface for device {device}")

