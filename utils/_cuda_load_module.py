
def _cuda_load_module(
    ptx: str | bytes, kernel_names: list[str] | None = None
) -> _CudaModule | dict[str, "_CudaKernel"]:
    """
    Loads a CUDA module from PTX code and returns a module object that can access kernels.

    Args:
        ptx (bytes or str): The PTX code to load
        kernel_names (list, optional): List of kernel names to extract from the module.
                                      If None, will return a module object with __getattr__.

    Returns:
        object: If kernel_names is None, returns a module object with __getattr__ to access kernels.
               If kernel_names is provided, returns a dict mapping kernel names to _CudaKernel objects.
    """
    # Ensure CUDA is initialized
    import torch.cuda

    # Load CUDA driver library
    libcuda = _get_gpu_runtime_library()

    # Convert PTX to bytes if it's a string
    if isinstance(ptx, str):
        ptx = ptx.encode("utf-8")

    # Load PTX module
    module = ctypes.c_void_p()
    # Get the current stream without directly importing torch.cuda at module level
    stream = torch.cuda.current_stream()
    with stream:
        _check_cuda(libcuda.cuModuleLoadData(ctypes.byref(module), ptx))

    if not kernel_names:
        return _CudaModule(module)

    # Return specific kernels
    kernels = {}
    for name in kernel_names:
        func = ctypes.c_void_p()
        _check_cuda(
            libcuda.cuModuleGetFunction(
                ctypes.byref(func), module, name.encode("utf-8")
            )
        )
        kernels[name] = _CudaKernel(func, module)
    return kernels

