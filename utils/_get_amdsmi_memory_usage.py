
def _get_amdsmi_memory_usage(device: Device = None) -> int:
    handle = _get_amdsmi_handler(device)
    return amdsmi.amdsmi_get_gpu_activity(handle)["umc_activity"]

