
def int_binary_op(
    name: str,
    c_function_name: str,
    return_type: RType = int_rprimitive,
    error_kind: int = ERR_NEVER,
) -> None:
    binary_op(
        name=name,
        arg_types=[int_rprimitive, int_rprimitive],
        return_type=return_type,
        c_function_name=c_function_name,
        error_kind=error_kind,
    )

