
def _get_amdsmi_device_memory_used(device: Device = None) -> int:
    handle = _get_amdsmi_handler(device)
    # amdsmi_get_gpu_vram_usage returns mem usage in megabytes
    mem_mega_bytes = amdsmi.amdsmi_get_gpu_vram_usage(handle)["vram_used"]
    mem_bytes = mem_mega_bytes * 1024 * 1024
    return mem_bytes

