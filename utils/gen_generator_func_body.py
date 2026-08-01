
def gen_generator_func_body(builder: IRBuilder, fn_info: FuncInfo, func_reg: Value | None) -> None:
    """Generate IR based on the body of a generator function.

    Add "__next__", "__iter__" and other generator methods to the generator
    class that implements the function (each function gets a separate class).

    Return the symbol table for the body.
    """
    builder.enter(fn_info, ret_type=object_rprimitive)
    setup_env_for_generator_class(builder)

    load_outer_envs(builder, builder.fn_info.generator_class)
    top_level = builder.top_level_fn_info()
    fitem = fn_info.fitem
    if (
        builder.fn_info.is_nested
        and isinstance(fitem, FuncDef)
        and top_level
        and top_level.add_nested_funcs_to_env
    ):
        setup_func_for_recursive_call(
            builder, fitem, builder.fn_info.generator_class, prefix=GENERATOR_ATTRIBUTE_PREFIX
        )
    create_switch_for_generator_class(builder)
    add_raise_exception_blocks_to_generator_class(builder, fitem.line)

    add_vars_to_env(builder, prefix=GENERATOR_ATTRIBUTE_PREFIX)

    builder.accept(fitem.body)
    builder.maybe_add_implicit_return()

    populate_switch_for_generator_class(builder)

    # Hang on to the local symbol table, since the caller will use it
    # to calculate argument defaults.
    symtable = builder.symtables[-1]

    args, _, blocks, ret_type, fn_info = builder.leave()

    add_methods_to_generator_class(builder, fn_info, args, blocks, fitem.is_coroutine)

    # Evaluate argument defaults in the surrounding scope, since we
    # calculate them *once* when the function definition is evaluated.
    calculate_arg_defaults(builder, fn_info, func_reg, symtable)

