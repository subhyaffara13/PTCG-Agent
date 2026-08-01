
def build_ir(
    modules: list[MypyFile],
    graph: Graph,
    types: dict[Expression, Type],
    mapper: Mapper,
    options: CompilerOptions,
    errors: Errors,
) -> ModuleIRs:
    """Build basic IR for a set of modules that have been type-checked by mypy.

    The returned IR is not complete and requires additional
    transformations, such as the insertion of refcount handling.
    """

    build_type_map(mapper, modules, graph, types, options, errors)
    adjust_generator_classes_of_methods(mapper)
    singledispatch_info = find_singledispatch_register_impls(modules, errors)

    result: ModuleIRs = {}
    if errors.num_errors > 0:
        return result

    # Generate IR for all modules.
    class_irs = []

    for module in modules:
        # First pass to determine free symbols.
        pbv = PreBuildVisitor(errors, module, singledispatch_info.decorators_to_remove, types)
        module.accept(pbv)

        # Declare generator classes for nested async functions and generators.
        for fdef in pbv.nested_funcs:
            if isinstance(fdef, FuncDef):
                # Make generator class name sufficiently unique.
                suffix = f"___{fdef.line}"
                if fdef.is_coroutine or fdef.is_generator:
                    create_generator_class_for_func(
                        module.fullname, None, fdef, mapper, name_suffix=suffix
                    )

        # Construct and configure builder objects (cyclic runtime dependency).
        visitor = IRBuilderVisitor()
        builder = IRBuilder(
            module.fullname,
            types,
            graph,
            errors,
            mapper,
            pbv,
            visitor,
            options,
            singledispatch_info.singledispatch_impls,
        )
        visitor.builder = builder

        # Second pass does the bulk of the work.
        transform_mypy_file(builder, module)
        module_ir = ModuleIR(
            module.fullname,
            list(builder.imports),
            builder.functions,
            builder.classes,
            builder.final_names,
            builder.type_var_names,
        )
        result[module.fullname] = module_ir
        class_irs.extend(builder.classes)

    analyze_always_defined_attrs(class_irs)

    # Compute vtables.
    for cir in class_irs:
        if cir.is_ext_class:
            compute_vtable(cir)

    return result

