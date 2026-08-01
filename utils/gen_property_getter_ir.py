
def gen_property_getter_ir(
    builder: IRBuilder, func_decl: FuncDecl, cdef: ClassDef, is_trait: bool
) -> FuncIR:
    """Generate an implicit trivial property getter for an attribute.

    These are used if an attribute can also be accessed as a property.
    """
    name = func_decl.name
    builder.enter(name)
    self_reg = builder.add_argument("self", func_decl.sig.args[0].type)
    line = func_decl._line or -1
    if not is_trait:
        value = builder.builder.get_attr(self_reg, name, func_decl.sig.ret_type, line)
        builder.add(Return(value, line))
    else:
        builder.add(Unreachable())
    args, _, blocks, ret_type, fn_info = builder.leave()
    return FuncIR(func_decl, args, blocks)

