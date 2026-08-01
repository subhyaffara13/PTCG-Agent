
def wrapper_function_header(fn: FuncIR, names: NameGenerator) -> str:
    """Return header of a vectorcall wrapper function.

    See comment above for a summary of the arguments.
    """
    assert not fn.internal
    return (
        "PyObject *{prefix}{name}("
        "PyObject *self, PyObject *const *args, size_t nargs, PyObject *kwnames)"
    ).format(prefix=PREFIX, name=fn.cname(names))

