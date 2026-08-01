
def get_dispatch_type(func: CallableType, register_arg: Type | None) -> Type | None:
    if register_arg is not None:
        return register_arg
    if func.arg_types:
        return func.arg_types[0]
    return None

