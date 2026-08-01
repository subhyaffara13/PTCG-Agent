
def cutlass_arch(device_type: str) -> str:
    if device_type == "xpu":
        arch = get_xpu_arch()
        return _normalize_xpu_arch(arch)
    else:
        arch = get_cuda_arch()
        return _normalize_cuda_arch(arch)

