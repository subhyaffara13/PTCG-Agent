
def _is_compiled() -> bool:
    r"""Return true if compile with CUDA support."""
    return hasattr(torch._C, "_cuda_getDeviceCount")


def _is_compiled() -> bool:
    r"""Return true if compiled with MTIA support."""
    return torch._C._mtia_isBuilt()


def _is_compiled() -> bool:
    r"""Return true if compile with XPU support."""
    return torch._C._has_xpu

