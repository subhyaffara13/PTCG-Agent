
def int_unary_op(name: str, c_function_name: str) -> PrimitiveDescription:
    return unary_op(
        name=name,
        arg_type=int_rprimitive,
        return_type=int_rprimitive,
        c_function_name=c_function_name,
        error_kind=ERR_NEVER,
    )

