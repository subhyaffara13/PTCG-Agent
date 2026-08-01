
def gen_glue(
    builder: IRBuilder,
    base_sig: FuncSignature,
    target: FuncIR,
    cls: ClassIR,
    base: ClassIR,
    fdef: FuncItem,
    *,
    do_py_ops: bool = False,
) -> FuncIR:
    """Generate glue methods that mediate between different method types in subclasses.

    Works on both properties and methods. See gen_glue_methods below
    for more details.

    If do_py_ops is True, then the glue methods should use generic
    C API operations instead of direct calls, to enable generating
    "shadow" glue methods that work with interpreted subclasses.
    """
    if fdef.is_property:
        return gen_glue_property(builder, base_sig, target, cls, base, fdef.line, do_py_ops)
    if do_py_ops and target.name.startswith(PROPSET_PREFIX):
        return gen_glue_property_setter(builder, base_sig, target, cls, base, fdef.line)
    return gen_glue_method(builder, base_sig, target, cls, base, fdef.line, do_py_ops)

