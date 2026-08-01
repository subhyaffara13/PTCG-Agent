
def _parse_kernel_fn_code(kernel_module_code: str) -> str:
    """
    The kernel_module_code is the python module that contains kernel function code.
    kernel function is the proper triton kernel function annotated with
    @triton.jit
    """
    from .codecache import PyCodeCache
    from .wrapper_benchmark import get_triton_kernel

    mod = PyCodeCache.load(kernel_module_code)
    kernel = get_triton_kernel(mod)
    # kernel is a CachingAutotune; kernel.fn is the JITFunction;
    # kernel.fn.fn is the function being decorate by triton.jit
    return inspect.getsource(kernel.fn.fn)

