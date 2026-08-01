
def add_property_methods_for_attribute_if_needed(
    info: TypeInfo,
    ir: ClassIR,
    attr_name: str,
    attr_rtype: RType,
    module_name: str,
    mapper: Mapper,
) -> None:
    """Add getter and/or setter for attribute if defined as property in a base class.

    Only add declarations. The body IR will be synthesized later during irbuild.
    """
    for base in info.mro[1:]:
        if base in mapper.type_to_ir:
            base_ir = mapper.type_to_ir[base]
            n = base.names.get(attr_name)
            if n is None:
                continue
            node = n.node
            if isinstance(node, Decorator) and node.name not in ir.method_decls:
                # Defined as a read-only property in base class/trait
                add_getter_declaration(ir, attr_name, attr_rtype, module_name)
            elif isinstance(node, OverloadedFuncDef) and is_valid_multipart_property_def(node):
                # Defined as a read-write property in base class/trait
                add_getter_declaration(ir, attr_name, attr_rtype, module_name)
                add_setter_declaration(ir, attr_name, attr_rtype, module_name)
            elif base_ir.is_trait and attr_rtype.error_overlap:
                add_getter_declaration(ir, attr_name, attr_rtype, module_name)
                add_setter_declaration(ir, attr_name, attr_rtype, module_name)

