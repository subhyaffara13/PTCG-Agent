
def set_torch_function_mode_stack(stack: list[Any]) -> None:
    for _ in range(_len_torch_function_stack()):
        _pop_torch_function_stack()

    for mode in stack:
        _push_on_torch_function_stack(mode)

