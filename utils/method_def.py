
def method_def(
    name: BaseOperatorName,
    module: str | None,
    overloads: Sequence[PythonSignatureNativeFunctionPair],
    *,
    method: bool,
) -> str:
    """
    Generate method def entry.
    """
    pycname = get_pycname(name)

    if name.dunder_method:
        # PyMethodDef entry for binary op, throws not implemented error
        pycname = f"TypeError_to_NotImplemented_<{pycname}>"

    if is_noarg(overloads):
        flags = "METH_NOARGS" if method else "METH_VARARGS | METH_KEYWORDS"
    else:
        pycname = f"castPyCFunctionWithKeywords({pycname})"
        flags = "METH_VARARGS | METH_KEYWORDS"

    if module == "torch":
        flags += " | METH_STATIC"

    return f'{{"{name}", {pycname}, {flags}, nullptr}},'

