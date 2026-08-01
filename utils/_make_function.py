
def _make_function(code, globals, name, argdefs, closure):
    # Setting __builtins__ in globals is needed for nogil CPython.
    globals["__builtins__"] = __builtins__
    return types.FunctionType(code, globals, name, argdefs, closure)

