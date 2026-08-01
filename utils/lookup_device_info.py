
def lookup_device_info(name: str) -> DeviceInfo | None:
    """
    Problem: when diffing profiles between amd and nvidia, we don't have access to the device information
    of the other one. Also, since the analysis is static, we should be able to do it on another device unrelated
    to the recorded device. Therefore, _device_mapping statically contains the information for lots of devices.
    If one is missing, please run DeviceInfo.get_device_info() and add it to _device_mapping.
      name (str): name of the device to lookup. Should map onto torch.cuda.get_device_name().
    """
    return _device_mapping.get(name)

