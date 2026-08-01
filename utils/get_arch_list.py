
def get_arch_list() -> list[str]:
    r"""Return list CUDA architectures this library was compiled for."""
    if not is_available():
        return []
    arch_flags = torch._C._cuda_getArchFlags()
    if arch_flags is None:
        return []
    return arch_flags.split()


def get_arch_list() -> list[str]:
    r"""Return list XPU architectures this library was compiled for."""
    if not _is_compiled():
        return []
    arch_flags = torch._C._xpu_getArchFlags()
    if arch_flags is None:
        return []
    return arch_flags.split()

