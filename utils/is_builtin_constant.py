
def is_builtin_constant(obj: Any) -> bool:
    return id(obj) in _builtin_constant_ids

