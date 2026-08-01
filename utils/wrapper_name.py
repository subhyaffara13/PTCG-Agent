
def wrapper_name(func: FunctionSchema) -> str:
    if func.name.overload_name:
        return f"{cpp.name(func)}_{func.name.overload_name}"
    else:
        return cpp.name(func)

