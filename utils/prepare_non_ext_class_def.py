
def prepare_non_ext_class_def(
    path: str,
    module_name: str,
    cdef: ClassDef,
    errors: Errors,
    mapper: Mapper,
    options: CompilerOptions,
) -> None:
    ir = mapper.type_to_ir[cdef.info]
    info = cdef.info

    for node in info.names.values():
        if isinstance(node.node, (FuncDef, Decorator)):
            prepare_method_def(ir, module_name, cdef, mapper, node.node, options)
        elif isinstance(node.node, OverloadedFuncDef):
            # Handle case for property with both a getter and a setter
            if node.node.is_property:
                if not is_valid_multipart_property_def(node.node):
                    errors.error("Unsupported property decorator semantics", path, cdef.line)
                for item in node.node.items:
                    prepare_method_def(ir, module_name, cdef, mapper, item, options)
            # Handle case for regular function overload
            else:
                prepare_method_def(ir, module_name, cdef, mapper, get_func_def(node.node), options)

        prepare_fast_path(ir, module_name, cdef, mapper, node.node, options)

    if any(cls in mapper.type_to_ir and mapper.type_to_ir[cls].is_ext_class for cls in info.mro):
        errors.error(
            "Non-extension classes may not inherit from extension classes", path, cdef.line
        )

