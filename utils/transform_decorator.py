
def transform_decorator(builder: IRBuilder, dec: Decorator) -> None:
    sig = builder.mapper.fdef_to_sig(dec.func, builder.options.strict_dunders_typing)
    func_ir, func_reg = gen_func_item(builder, dec.func, dec.func.name, sig)
    decorated_func: Value | None = None
    if func_reg:
        decorated_func = load_decorated_func(builder, dec.func, func_reg)
        builder.assign(get_func_target(builder, dec.func), decorated_func, dec.func.line)
    # If the prebuild pass didn't put this function in the function to decorators map (for example
    # if this is a registered singledispatch implementation with no other decorators), we should
    # treat this function as a regular function, not a decorated function
    elif dec.func in builder.fdefs_to_decorators:
        # Obtain the function name in order to construct the name of the helper function.
        name = dec.func.fullname.split(".")[-1]

        # Load the callable object representing the non-decorated function, and decorate it.
        orig_func = builder.load_global_str(name, dec.line)
        decorated_func = load_decorated_func(builder, dec.func, orig_func)

    if decorated_func is not None:
        # Set the callable object representing the decorated function as a global.
        builder.call_c(
            exact_dict_set_item_op,
            [builder.load_globals_dict(), builder.load_str(dec.func.name), decorated_func],
            decorated_func.line,
        )

    maybe_insert_into_registry_dict(builder, dec.func)

    builder.functions.append(func_ir)

