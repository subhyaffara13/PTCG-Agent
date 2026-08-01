
def _nvshmem_init_hook(*args, **kwargs) -> None:  # type: ignore[no-untyped-def]
    """
    A hook function to initialize the CUModule created by `triton.jit` with
    NVSHMEM device context
    """
    from torch._C._distributed_c10d import _nvshmemx_cumodule_init

    jit_function = kwargs["fn"].jit_function
    fn_name = jit_function.fn.__name__

    # Only initialize NVSHMEM module for kernels registered via @requires_nvshmem
    if NvshmemKernelRegistry.has(fn_name):
        key = kwargs["key"]
        device = kwargs["compile"]["device"]
        jit_function = kwargs["fn"].jit_function
        kernel_cache = jit_function.device_caches[device][0]
        kernel = kernel_cache.get(key, None)
        if kernel is not None:
            kernel.run
            # Initialize NVSHMEM for the CU module
            _nvshmemx_cumodule_init(kernel.module)
        else:
            logger.warning(
                f"It seems Triton hasn't created a kernel for function {fn_name}. "  # noqa: G004
                "Please report this issue to Triton."
            )

