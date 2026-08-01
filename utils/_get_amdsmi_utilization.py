
def _get_amdsmi_utilization(device: Device = None) -> int:
    handle = _get_amdsmi_handler(device)
    return amdsmi.amdsmi_get_gpu_activity(handle)["gfx_activity"]

