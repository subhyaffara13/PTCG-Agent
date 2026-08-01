
def _get_fused_kernels_supported_devices() -> list[str]:
    r"""Return the device type list that supports fused kernels in optimizer."""
    return [
        "mps",
        "cuda",
        "xpu",
        "hpu",
        "cpu",
        "mtia",
        torch._C._get_privateuse1_backend_name(),
    ]

