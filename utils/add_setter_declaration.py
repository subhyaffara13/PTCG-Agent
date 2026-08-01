
def add_setter_declaration(
    ir: ClassIR, attr_name: str, attr_rtype: RType, module_name: str
) -> None:
    self_arg = RuntimeArg("self", RInstance(ir), pos_only=True)
    value_arg = RuntimeArg("value", attr_rtype, pos_only=True)
    sig = FuncSignature([self_arg, value_arg], none_rprimitive)
    setter_name = PROPSET_PREFIX + attr_name
    decl = FuncDecl(setter_name, ir.name, module_name, sig, FUNC_NORMAL)
    decl.is_prop_setter = True
    decl.implicit = True  # Triggers synthesization
    ir.method_decls[setter_name] = decl

