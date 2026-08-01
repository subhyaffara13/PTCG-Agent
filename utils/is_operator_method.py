
def is_operator_method(fullname: str | None) -> bool:
    if not fullname:
        return False
    short_name = fullname.split(".")[-1]
    return (
        short_name in operators.op_methods.values()
        or short_name in operators.reverse_op_methods.values()
        or short_name in operators.unary_op_methods.values()
    )

