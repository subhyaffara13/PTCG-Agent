
def _get_current_dispatch_mode() -> TorchDispatchMode | None:
    """
    Return the top user mode on the stack (the next one that would be
    executed) if there are any.
    """
    stack_len = _len_torch_dispatch_stack()
    if stack_len > 0:
        return _get_dispatch_stack_at(stack_len - 1)
    return None

