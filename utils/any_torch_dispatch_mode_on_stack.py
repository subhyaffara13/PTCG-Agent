
def any_torch_dispatch_mode_on_stack() -> bool:
    stack_len = torch._C._len_torch_dispatch_stack()

    for idx in range(stack_len):
        mode = _get_dispatch_stack_at(idx)

        # Apply filters first
        if mode.is_infra_mode():
            continue

        if mode.ignore_compile_internals():
            continue

        return True
    return False

