
def build_type_map(
    mapper: Mapper,
    modules: list[MypyFile],
    graph: Graph,
    types: dict[Expression, Type],
    options: CompilerOptions,
    errors: Errors,
) -> None:
    # Collect all classes defined in everything we are compiling
    classes = []
    for module in modules:
        module_classes = [node for node in module.defs if isinstance(node, ClassDef)]
        classes.extend([(module, cdef) for cdef in module_classes])

    # Collect all class mappings so that we can bind arbitrary class name
    # references even if there are import cycles.
    for module, cdef in classes:
        class_ir = ClassIR(
            cdef.name,
            module.fullname,
            is_trait(cdef),
            is_abstract=cdef.info.is_abstract,
            is_final_class=cdef.info.is_final,
        )
        class_ir.is_ext_class = is_extension_class(module.path, cdef, errors)
        if class_ir.is_ext_class:
            class_ir.deletable = cdef.info.deletable_attributes.copy()
        # If global optimizations are disabled, turn of tracking of class children
        if not options.global_opts:
            class_ir.children = None
        mapper.type_to_ir[cdef.info] = class_ir
        mapper.symbol_fullnames.add(class_ir.fullname)
        class_ir.is_enum = cdef.info.is_enum and len(cdef.info.enum_members) > 0

    # Populate structural information in class IR for extension classes.
    for module, cdef in classes:
        with catch_errors(module.path, cdef.line):
            if mapper.type_to_ir[cdef.info].is_ext_class:
                prepare_class_def(module.path, module.fullname, cdef, errors, mapper, options)
            else:
                prepare_non_ext_class_def(
                    module.path, module.fullname, cdef, errors, mapper, options
                )

    # Validate cross-class properties after all ClassIR flags are populated.
    for module, cdef in classes:
        with catch_errors(module.path, cdef.line):
            if mapper.type_to_ir[cdef.info].is_ext_class:
                validate_acyclic_class_bases(module.path, cdef, errors, mapper)

    # Prepare implicit attribute accessors as needed if an attribute overrides a property.
    for module, cdef in classes:
        class_ir = mapper.type_to_ir[cdef.info]
        if class_ir.is_ext_class:
            prepare_implicit_property_accessors(cdef.info, class_ir, module.fullname, mapper)

    # Register __mypyc_defaults_setup FuncDecls on classes that have their own
    # class-level default attribute assignments. Done here, before any IR build
    # runs, so that the cross-class lookup in generate_attr_defaults_init is
    # order-independent: IR build within a compilation group proceeds in
    # filename order, so a subclass may be IR-built before its base.
    for module, cdef in classes:
        class_ir = mapper.type_to_ir[cdef.info]
        if class_ir.is_ext_class and _has_own_default_attrs(cdef, class_ir):
            _register_defaults_setup_decl(class_ir, module.fullname)

    # Validate __deletable__ declarations. Done here so the compiler exits
    # early on invalid input before any IR is built.
    for module, cdef in classes:
        class_ir = mapper.type_to_ir[cdef.info]
        if class_ir.is_ext_class:
            with catch_errors(module.path, cdef.line):
                _check_deletable_declarations(module.path, cdef, class_ir, errors)

    # Collect all the functions also. We collect from the symbol table
    # so that we can easily pick out the right copy of a function that
    # is conditionally defined. This doesn't include nested functions!
    for module in modules:
        for func in get_module_func_defs(module):
            prepare_func_def(module.fullname, None, func, mapper, options)
            # TODO: what else?

    # Check for incompatible attribute definitions that were not
    # flagged by mypy but can't be supported when compiling.
    for module, cdef in classes:
        class_ir = mapper.type_to_ir[cdef.info]
        for attr in class_ir.attributes:
            for base_ir in class_ir.mro[1:]:
                if attr in base_ir.attributes:
                    if not is_same_type(class_ir.attributes[attr], base_ir.attributes[attr]):
                        node = cdef.info.names[attr].node
                        assert node is not None
                        kind = "trait" if base_ir.is_trait else "class"
                        errors.error(
                            f'Type of "{attr}" is incompatible with '
                            f'definition in {kind} "{base_ir.name}"',
                            module.path,
                            node.line,
                        )

