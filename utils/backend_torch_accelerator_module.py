
def backend_torch_accelerator_module(device: str):
    return _device_agnostic_dispatch(device, BACKEND_TORCH_ACCELERATOR_MODULE)

