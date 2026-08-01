
def add_getter_declaration(
    ir: ClassIR, attr_name: str, attr_rtype: RType, module_name: str
) -> None:
    self_arg = RuntimeArg("self", RInstance(ir), pos_only=True)
    sig = FuncSignature([self_arg], attr_rtype)
    decl = FuncDecl(attr_name, ir.name, module_name, sig, FUNC_NORMAL)
    decl.is_prop_getter = True
    decl.implicit = True  # Triggers synthesization
    ir.method_decls[attr_name] = decl
    ir.property_types[attr_name] = attr_rtype  # TODO: Needed??

