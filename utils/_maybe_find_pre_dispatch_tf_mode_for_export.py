
def _maybe_find_pre_dispatch_tf_mode_for_export():
    if not torch._C._is_torch_function_mode_enabled():
        return None

    torch_function_mode_stack = torch.overrides._get_current_function_mode_stack()

    pre_dispatch_tf_modes = [
        mode
        for mode in torch_function_mode_stack
        if isinstance(mode, PreDispatchTorchFunctionMode)
    ]

    if len(pre_dispatch_tf_modes) > 1:
        raise AssertionError(
            f"Expected only one PreDispatchTorchFunctionMode, found {len(pre_dispatch_tf_modes)}"
        )

    if len(pre_dispatch_tf_modes) == 0:
        return None

    mode = pre_dispatch_tf_modes[0]
    return mode

