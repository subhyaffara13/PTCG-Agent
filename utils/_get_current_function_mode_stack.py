
def _get_current_function_mode_stack():
    stack_len = _len_torch_function_stack()
    return [_get_function_stack_at(i) for i in range(stack_len)]

