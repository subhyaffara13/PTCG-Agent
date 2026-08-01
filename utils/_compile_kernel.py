
def _compile_kernel(
    kernel_source: str,
    kernel_name: str,
    compute_capability: str | None = None,
    cuda_include_dirs: list | None = None,
    nvcc_options: list | None = None,
):
    """
    Compiles a CUDA kernel using NVRTC and returns a callable function.

    This function is a wrapper for NVRTC that enables runtime compilation of CUDA kernels.
    Note that this returns a raw CUDA kernel that operates on raw memory pointers.
    To use this kernel as a proper PyTorch operator, you should wrap it following the guide at:
    pytorch.org/tutorials/advanced/python_custom_ops.html

    Args:
        kernel_source (str): The CUDA kernel source code as a string
        kernel_name (str): The name of the kernel function to compile
        compute_capability (str, optional): The compute capability to target (e.g., "86").
                                           If None, will detect from current device.
        cuda_include_dirs (list, optional): List of directories containing CUDA headers
        nvcc_options (list, optional): Additional options to pass to NVRTC

    Returns:
        callable: A Python function that can be called with PyTorch tensor arguments to execute the kernel

    Example:
        >>> # xdoctest: +SKIP
        >>> kernel_code = '''
        extern "C"
        __global__ void add_tensors(const float* a, const float* b, float* c, int n) {
            int i = threadIdx.x + blockIdx.x * blockDim.x;
            if (i < n)
                c[i] = a[i] + b[i];
        }
        '''
        >>> add_kernel = torch.cuda.compile_kernel(kernel_code, "add_tensors")
        >>> a = torch.randn(1024, device="cuda")
        >>> b = torch.randn(1024, device="cuda")
        >>> c = torch.empty_like(a)
        >>> add_kernel(grid=(4, 1, 1), block=(256, 1, 1), args=[a, b, c, a.numel()])
    """
    from torch.cuda._utils import _cuda_load_module, _nvrtc_compile

    # Compile the kernel to PTX
    ptx, mangled_name = _nvrtc_compile(
        kernel_source,
        kernel_name,
        compute_capability,
        cuda_include_dirs,
        nvcc_options,
    )

    # Load the module and get the kernel
    result = _cuda_load_module(ptx, [mangled_name])

    if isinstance(result, dict):
        return result[mangled_name]
    else:
        # This branch shouldn't be executed if kernel_names is provided,
        # but MyPy needs this to understand type narrowing
        return getattr(result, mangled_name)

