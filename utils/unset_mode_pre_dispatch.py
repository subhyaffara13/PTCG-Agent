
def unset_mode_pre_dispatch(mode_key, schema_check=False):
    current_mode_stack_pre_dispatch = mode_stack_state_for_pre_dispatch()
    valid_keys = (
        torch._C._TorchDispatchModeKey.PROXY,
        torch._C._TorchDispatchModeKey.FUNCTIONAL,
    )
    if mode_key is not None and mode_key not in valid_keys:
        raise AssertionError(
            f"mode_key must be None or one of {valid_keys}, got {mode_key}"
        )
    if schema_check:
        if mode_key is not None:
            raise AssertionError("mode_key must be None when schema_check is True")

    def _unset_mode():
        # NOTE: Using `is` rather than `==` to work around slow enum comparison in
        # pybind11.
        if mode_key is torch._C._TorchDispatchModeKey.PROXY:
            current_mode = current_mode_stack_pre_dispatch.get(0)
            mode_stack_state_for_pre_dispatch().set(0, None)
            return current_mode
        elif mode_key is torch._C._TorchDispatchModeKey.FUNCTIONAL:
            current_mode = current_mode_stack_pre_dispatch.get(1)
            mode_stack_state_for_pre_dispatch().set(1, None)
            return current_mode
        else:
            current_mode = mode_stack_state_for_pre_dispatch()._schema_check_mode
            mode_stack_state_for_pre_dispatch()._schema_check_mode = None
            return current_mode

    current_mode = _unset_mode()

    new_pre_dispatch_len = _len_torch_dispatch_stack_pre_dispatch()
    # When we are unsetting a mode, we need to check if there is
    # active mode left on the PreDispatch key. If there is nothing
    # active, we need to remove PreDispatch key from local dispatch include
    # set.
    if new_pre_dispatch_len == 0:
        torch._C._dispatch_tls_set_dispatch_key_included(DispatchKey.PreDispatch, False)

    return current_mode

