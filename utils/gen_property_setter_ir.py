
def gen_property_setter_ir(
    builder: IRBuilder, func_decl: FuncDecl, cdef: ClassDef, is_trait: bool
) -> FuncIR:
    """Generate an implicit trivial property setter for an attribute.

    These are used if an attribute can also be accessed as a property.
    """
    name = func_decl.name
    builder.enter(name)
    self_reg = builder.add_argument("self", func_decl.sig.args[0].type)
    value_reg = builder.add_argument("value", func_decl.sig.args[1].type)
    assert name.startswith(PROPSET_PREFIX)
    attr_name = name[len(PROPSET_PREFIX) :]
    line = func_decl._line or -1
    if not is_trait:
        builder.add(SetAttr(self_reg, attr_name, value_reg, line))
    builder.add(Return(builder.none(), line))
    args, _, blocks, ret_type, fn_info = builder.leave()
    return FuncIR(func_decl, args, blocks, line)

