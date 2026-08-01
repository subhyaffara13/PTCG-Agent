
def start_kernel_compile(
    pending_kernels: dict[str, Any], kernel_name: str, kernel_source: str
) -> None:
    """
    This function is called from C++ at model initialization time for each kernel.
    It starts the compilation in a background process but does NOT wait for it.
    The actual kernel execution happens later in run_triton_kernel_with_autotune().

    The pending_kernels dict is per-module, created in C++ and passed through
    to avoid global state collisions across compiled modules.
    """
    if kernel_name in pending_kernels:
        return

    async_compile = _get_async_compile()  # noqa: F841 (used by eval below)

    # Evaluate the kernel source to get the Future or CachingAutotuner
    # The kernel_source is like: async_compile.triton('name', '''...''', ...)
    kernel_obj = eval(kernel_source.strip())  # noqa: S307

    pending_kernels[kernel_name] = kernel_obj

