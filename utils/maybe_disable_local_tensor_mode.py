
def maybe_disable_local_tensor_mode() -> contextlib.AbstractContextManager:
    """
    Context manager that disables LocalTensorMode for the duration of the context.
    """
    lm = local_tensor_mode()
    return lm.disable() if lm is not None else contextlib.nullcontext()

