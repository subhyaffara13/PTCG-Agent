
def args_have_same_dtype(args):
    if not args:
        raise AssertionError("args must be non-empty")
    base_dtype = _type_utils.JitScalarType.from_value(args[0])
    has_same_dtype = all(
        _type_utils.JitScalarType.from_value(elem) == base_dtype for elem in args
    )
    return has_same_dtype

