
def backend_synchronize(device: str):
    return _device_agnostic_dispatch(device, BACKEND_SYNCHRONIZE)

