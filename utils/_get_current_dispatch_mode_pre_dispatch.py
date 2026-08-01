
def _get_current_dispatch_mode_pre_dispatch():
    if mode_stack_state_for_pre_dispatch()._schema_check_mode is not None:
        return mode_stack_state_for_pre_dispatch()._schema_check_mode
    else:
        stack_len = mode_stack_state_for_pre_dispatch().count()
        if stack_len == 2:
            return mode_stack_state_for_pre_dispatch().get(1)
        if stack_len == 1:
            return (
                mode_stack_state_for_pre_dispatch().get(1)
                if mode_stack_state_for_pre_dispatch().get(1) is not None
                else mode_stack_state_for_pre_dispatch().get(0)
            )
    return None

