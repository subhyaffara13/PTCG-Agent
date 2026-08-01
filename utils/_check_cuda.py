
def _check_cuda(result: int) -> None:
    if result == 0:
        return
    err_str = ctypes.c_char_p()
    libcuda = _get_gpu_runtime_library()  # Get reference to CUDA library
    libcuda.cuGetErrorString(result, ctypes.byref(err_str))
    error_message = (
        err_str.value.decode() if err_str.value is not None else "Unknown CUDA error"
    )
    raise RuntimeError(f"CUDA error: {error_message}")

