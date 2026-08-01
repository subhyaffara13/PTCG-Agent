
def get_prev_stack_var_name() -> str:
    from ..bytecode_transformation import unique_id

    return unique_id("___prev_torch_function_mode_stack")

