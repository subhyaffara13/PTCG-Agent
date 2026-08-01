
def _get_const(value, desc, arg_name):
    if not _is_constant(value):
        raise errors.SymbolicValueError(
            f"ONNX symbolic expected a constant value of the '{arg_name}' argument, "
            f"got '{value}'",
            value,
        )
    return _parse_arg(value, desc)

