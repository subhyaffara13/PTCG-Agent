
def set_wrap_triton_enabled(enabled: bool) -> Generator[None, None, None]:
    """If triton kernels annotated with @wrap_triton should dispatch via HOP
    or go straight to the triton kernel execution.

    We have this switch because eager-mode performance of HOP dispatch is slow
    enough to matter (~1ms) and we know that wrap_triton isn't necessary in
    some situations (eager-mode with regular Tensors)
    """
    try:
        prev = is_wrap_triton_enabled()
        wrap_triton_enabled.value = enabled
        yield
    finally:
        wrap_triton_enabled.value = prev

