
def _get_dispatch_mode_pre_dispatch(mode_key):
    # NOTE: Using `is` rather than `==` to work around slow enum comparison in pybind11.
    if mode_key is torch._C._TorchDispatchModeKey.PROXY:
        return mode_stack_state_for_pre_dispatch().get(0)
    else:
        if mode_key is not torch._C._TorchDispatchModeKey.FUNCTIONAL:
            raise AssertionError(
                f"mode_key must be PROXY or FUNCTIONAL, got {mode_key}"
            )
        return mode_stack_state_for_pre_dispatch().get(1)

