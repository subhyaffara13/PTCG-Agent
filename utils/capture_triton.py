
def capture_triton(triton_kernel: Callable, /) -> Any:
    """This API has been renamed to wrap_triton"""
    return wrap_triton(triton_kernel)

