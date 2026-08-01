
def getRocmVersion() -> tuple[int, int]:
    from torch.testing._internal.common_cuda import _get_torch_rocm_version
    rocm_version = _get_torch_rocm_version()
    return (rocm_version[0], rocm_version[1])

