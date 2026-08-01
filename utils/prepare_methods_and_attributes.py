
def prepare_methods_and_attributes(
    cdef: ClassDef,
    ir: ClassIR,
    path: str,
    module_name: str,
    errors: Errors,
    mapper: Mapper,
    options: CompilerOptions,
) -> None:
    """Populate attribute and method declarations."""
    info = cdef.info
    for name, node in info.names.items():
        # Currently all plugin generated methods are dummies and not included.
        if node.plugin_generated:
            continue

        if isinstance(node.node, Var):
            assert node.node.type, "Class member %s missing type" % name
            if not node.node.is_classvar and name not in ("__slots__", "__deletable__"):
                attr_rtype = mapper.type_to_rtype(node.node.type)
                if ir.is_trait and attr_rtype.error_overlap:
                    # Traits don't have attribute definedness bitmaps, so use
                    # property accessor methods to access attributes that need them.
                    # We will generate accessor implementations that use the class bitmap
                    # for any concrete subclasses.
                    add_getter_declaration(ir, name, attr_rtype, module_name)
                    add_setter_declaration(ir, name, attr_rtype, module_name)
                ir.attributes[name] = attr_rtype
                if node.node.is_final:
                    ir.final_attributes.add(name)
        elif isinstance(node.node, (FuncDef, Decorator)):
            prepare_method_def(ir, module_name, cdef, mapper, node.node, options)
        elif isinstance(node.node, OverloadedFuncDef):
            # Handle case for property with both a getter and a setter
            if node.node.is_property:
                if is_valid_multipart_property_def(node.node):
                    for item in node.node.items:
                        prepare_method_def(ir, module_name, cdef, mapper, item, options)
                else:
                    errors.error("Unsupported property decorator semantics", path, cdef.line)

            # Handle case for regular function overload
            else:
                if not node.node.impl:
                    errors.error(
                        "Overloads without implementation are not supported", path, cdef.line
                    )
                else:
                    prepare_method_def(ir, module_name, cdef, mapper, node.node.impl, options)

    if ir.builtin_base:
        ir.attributes.clear()

