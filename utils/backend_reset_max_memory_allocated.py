
def backend_reset_max_memory_allocated(device: str):
    return _device_agnostic_dispatch(device, BACKEND_RESET_MAX_MEMORY_ALLOCATED)

