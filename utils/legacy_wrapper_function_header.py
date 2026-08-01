
def legacy_wrapper_function_header(fn: FuncIR, names: NameGenerator) -> str:
    return "PyObject *{prefix}{name}(PyObject *self, PyObject *args, PyObject *kw)".format(
        prefix=PREFIX, name=fn.cname(names)
    )

