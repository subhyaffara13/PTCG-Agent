
def call_module_hooks_from_backward_state(
    _: Any, result: Any, *args: Any, bw_state: Any, hooks_name: str, module_name: str
) -> Any:
    module = getattr(bw_state, module_name)
    hooks = getattr(bw_state, hooks_name)
    for hook in hooks:
        new_result = hook(module, result, *args)
        if new_result is not None:
            result = new_result
    return result

