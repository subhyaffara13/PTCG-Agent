
def for_function(callee: CallableType) -> str:
    name = callable_name(callee)
    if name is not None:
        return f" for {name}"
    return ""

