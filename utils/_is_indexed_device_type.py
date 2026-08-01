
def _is_indexed_device_type(device_type: str) -> bool:
    return device_type in [
        "cuda",
        "hpu",
        "xpu",
        "mps",
        "mtia",
        torch._C._get_privateuse1_backend_name(),
    ]

