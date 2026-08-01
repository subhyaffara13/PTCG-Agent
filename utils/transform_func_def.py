
def transform_func_def(builder: IRBuilder, fdef: FuncDef) -> None:
    sig = builder.mapper.fdef_to_sig(fdef, builder.options.strict_dunders_typing)
    func_ir, func_reg = gen_func_item(builder, fdef, fdef.name, sig)

    # If the function that was visited was a nested function, then either look it up in our
    # current environment or define it if it was not already defined.
    if func_reg:
        builder.assign(get_func_target(builder, fdef), func_reg, fdef.line)
    maybe_insert_into_registry_dict(builder, fdef)
    builder.add_function(func_ir, fdef.line)

