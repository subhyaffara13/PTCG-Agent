
def maybe_insert_into_registry_dict(builder: IRBuilder, fitem: FuncDef) -> None:
    line = fitem.line
    is_singledispatch_main_func = fitem in builder.singledispatch_impls
    # dict of singledispatch_func to list of register_types (fitem is the function to register)
    to_register: defaultdict[FuncDef, list[TypeInfo]] = defaultdict(list)
    for main_func, impls in builder.singledispatch_impls.items():
        for dispatch_type, impl in impls:
            if fitem == impl:
                to_register[main_func].append(dispatch_type)

    if not to_register and not is_singledispatch_main_func:
        return

    if is_singledispatch_main_func:
        main_func_name = singledispatch_main_func_name(fitem.name)
        main_func_obj = load_func(builder, main_func_name, fitem.fullname, line)

        loaded_object_type = builder.load_module_attr_by_fullname("builtins.object", line)
        registry_dict = builder.builder.make_dict([(loaded_object_type, main_func_obj)], line)

        dispatch_func_obj = builder.load_global_str(fitem.name, line)
        builder.primitive_op(
            py_setattr_op, [dispatch_func_obj, builder.load_str("registry"), registry_dict], line
        )

    for singledispatch_func, types in to_register.items():
        # TODO: avoid recomputing the native IDs for all the functions every time we find a new
        # function
        native_ids = get_native_impl_ids(builder, singledispatch_func)
        if fitem not in native_ids:
            to_insert = load_func(builder, fitem.name, fitem.fullname, line)
        else:
            current_id = native_ids[fitem]
            load_literal = LoadLiteral(current_id, object_rprimitive)
            to_insert = builder.add(load_literal)
        # TODO: avoid reloading the registry here if we just created it
        dispatch_func_obj = load_func(
            builder, singledispatch_func.name, singledispatch_func.fullname, line
        )
        registry = load_singledispatch_registry(builder, dispatch_func_obj, line)
        for typ in types:
            loaded_type = load_type(builder, typ, None, line)
            builder.call_c(exact_dict_set_item_op, [registry, loaded_type, to_insert], line)
        dispatch_cache = builder.builder.get_attr(
            dispatch_func_obj, "dispatch_cache", dict_rprimitive, line
        )
        builder.gen_method_call(dispatch_cache, "clear", [], None, line)

