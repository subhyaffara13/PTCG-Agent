
def toolkit_version(device_type: str) -> str:
    if device_type == "xpu":
        return get_xpu_version()
    else:
        return get_cuda_version()

