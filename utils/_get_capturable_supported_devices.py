
def _get_capturable_supported_devices(supports_xla: bool = True) -> list[str]:
    r"""Return the device type list that supports capturable optimizer."""
    capturable_supported_devices = ["cuda", "xpu", "hpu"]
    if not torch.jit.is_scripting():
        capturable_supported_devices.append(torch._C._get_privateuse1_backend_name())
    if supports_xla:
        capturable_supported_devices.append("xla")
    return capturable_supported_devices

