
def maybe_create_output(f: NativeFunction, var_name: str) -> str:
    if len(f.func.returns) == 0:
        return ""
    return_type = dispatcher.returns_type(f.func.returns).remove_const_ref().cpp_type()
    return f"{return_type} {var_name} = "

