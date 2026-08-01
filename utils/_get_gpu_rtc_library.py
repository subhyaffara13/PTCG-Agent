
def _get_gpu_rtc_library() -> ctypes.CDLL:
    # Since PyTorch already loads the GPU RTC library, we can use the system library
    # which should be compatible with PyTorch's version
    if torch.version.hip:
        return _get_hiprtc_library()
    else:
        return _get_nvrtc_library()

