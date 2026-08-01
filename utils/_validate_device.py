
def _validate_device(location, backend_name):
    """
    Check whether the device index of specified backend is valid

    In case of privateuse1 backend, your must first register a device_module for
    privateuse1 using torch._register_device_module. Implement the following
    methods in device_module like cuda: device_module._utils._get_device_index(location, True),
    device_module.device_count().

    Args:
        location: string of device
        backend_name: the backend name or the name of privateuse1, which can be renamed

    Returns:
        device_index: int
    """
    if not hasattr(torch, backend_name):
        raise RuntimeError(
            f"The {backend_name.upper()} device module is not registered. "
            "If you are running on a CPU-only machine, "
            "please use torch.load with map_location=torch.device('cpu') "
            "to map your storages to the CPU."
        )
    device_module = getattr(torch, backend_name)
    if hasattr(device_module, "_utils") and hasattr(
        device_module._utils, "_get_device_index"
    ):
        device_index = device_module._utils._get_device_index(location, True)
        device = torch.device(backend_name, device_index)
    else:
        device = torch.device(location)
        device_index = device.index if device.index else 0
    if hasattr(device_module, "is_available") and not device_module.is_available():
        raise RuntimeError(
            f"Attempting to deserialize object on a {backend_name.upper()} "
            f"device but torch.{backend_name}.is_available() is False. "
            "If you are running on a CPU-only machine, "
            "please use torch.load with map_location=torch.device('cpu') "
            "to map your storages to the CPU."
        )
    if hasattr(device_module, "device_count"):
        device_count = device_module.device_count()
        if device_index >= device_count:
            raise RuntimeError(
                f"Attempting to deserialize object on {backend_name.upper()} device "
                f"{device_index} but torch.{backend_name}.device_count() is {device_count}. "
                "Please use torch.load with map_location to map your storages "
                "to an existing device."
            )
    return device


def _validate_device(query: Tensor, key: Tensor, value: Tensor) -> None:
    """TODO: Remove once non cuda/cpu devices support is added
    We only need to check query since we have already that q,k,v are on the same device
    """
    if query.device.type == "cpu" and (
        query.requires_grad or key.requires_grad or value.requires_grad
    ):
        raise NotImplementedError(
            "FlexAttention does not support backward on CPU. Please set the input requires_grad to False or use another device."
        )
    supported_devices = {"cuda", "cpu", "xpu", "hpu"}
    if query.device.type not in supported_devices:
        raise ValueError(
            "FlexAttention is only supported on CUDA, CPU or HPU devices. "
            f"Found input tensors on {query.device.type} device."
        )

