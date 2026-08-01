
def _pop_mode_from_pre_dispatch():
    mode_stack = mode_stack_state_for_pre_dispatch()
    pre_dispatch_len = _len_torch_dispatch_stack_pre_dispatch()

    if pre_dispatch_len == 0:
        raise AssertionError("Trying to pop empty mode stack")

    if mode_stack._schema_check_mode is not None:
        return unset_mode_pre_dispatch(None, schema_check=True)
    if mode_stack.get(1) is not None:
        return unset_mode_pre_dispatch(torch._C._TorchDispatchModeKey.FUNCTIONAL)
    if mode_stack.get(0) is not None:
        return unset_mode_pre_dispatch(torch._C._TorchDispatchModeKey.PROXY)

