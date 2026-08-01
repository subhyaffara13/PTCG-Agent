
def _get_gpu_runtime_library() -> ctypes.CDLL:
    if torch.version.hip:
        return _get_hip_runtime_library()
    else:
        return _get_cuda_library()

