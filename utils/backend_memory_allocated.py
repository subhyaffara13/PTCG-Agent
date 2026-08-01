
def backend_memory_allocated(device: str):
    return _device_agnostic_dispatch(device, BACKEND_MEMORY_ALLOCATED)

