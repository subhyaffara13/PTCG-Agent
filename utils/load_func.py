
def load_func(builder: IRBuilder, func_name: str, fullname: str | None, line: int) -> Value:
    if fullname and not fullname.startswith(builder.current_module):
        # we're calling a function in a different module

        # We can't use load_module_attr_by_fullname here because we need to load the function using
        # func_name, not the name specified by fullname (which can be different for underscore
        # function)
        module = fullname.rsplit(".")[0]
        loaded_module = builder.load_module(module)

        func = builder.py_get_attr(loaded_module, func_name, line)
    else:
        func = builder.load_global_str(func_name, line)
    return func

