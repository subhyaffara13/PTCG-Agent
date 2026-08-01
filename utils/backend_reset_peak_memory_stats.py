
def backend_reset_peak_memory_stats(device: str):
    return _device_agnostic_dispatch(device, BACKEND_RESET_PEAK_MEMORY_STATS)

