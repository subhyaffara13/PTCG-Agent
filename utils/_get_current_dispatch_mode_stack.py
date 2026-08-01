
def _get_current_dispatch_mode_stack() -> list[TorchDispatchMode]:
    """
    Returns the current stack of dispatch modes, with the most recent
    (i.e., the one that will be processed first) at the end of the
    list (standard stack convention).
    """
    stack_len = _len_torch_dispatch_stack()
    return [_get_dispatch_stack_at(i) for i in range(stack_len)]

