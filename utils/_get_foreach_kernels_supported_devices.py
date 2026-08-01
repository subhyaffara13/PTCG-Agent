
def _get_foreach_kernels_supported_devices() -> list[str]:
    r"""Return the device type list that supports foreach kernels."""
    return ["cuda", "xpu", "mtia", torch._C._get_privateuse1_backend_name()]

