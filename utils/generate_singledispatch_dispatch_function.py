
def generate_singledispatch_dispatch_function(
    builder: IRBuilder, main_singledispatch_function_name: str, fitem: FuncDef
) -> None:
    line = fitem.line
    current_func_decl = builder.mapper.func_to_decl[fitem]
    arg_info = get_args(builder, current_func_decl.sig.args, line)

    dispatch_func_obj = builder.self()

    arg_type = builder.builder.get_type_of_obj(arg_info.args[0], line)
    dispatch_cache = builder.builder.get_attr(
        dispatch_func_obj, "dispatch_cache", dict_rprimitive, line
    )
    call_find_impl, use_cache, call_func = BasicBlock(), BasicBlock(), BasicBlock()
    get_result = builder.primitive_op(dict_get_method_with_none, [dispatch_cache, arg_type], line)
    is_not_none = builder.translate_is_op(get_result, builder.none_object(), "is not", line)
    impl_to_use = Register(object_rprimitive)
    builder.add_bool_branch(is_not_none, use_cache, call_find_impl)

    builder.activate_block(use_cache)
    builder.assign(impl_to_use, get_result, line)
    builder.goto(call_func)

    builder.activate_block(call_find_impl)
    find_impl = builder.load_module_attr_by_fullname("functools._find_impl", line)
    registry = load_singledispatch_registry(builder, dispatch_func_obj, line)
    uncached_impl = builder.py_call(find_impl, [arg_type, registry], line)
    builder.call_c(exact_dict_set_item_op, [dispatch_cache, arg_type, uncached_impl], line)
    builder.assign(impl_to_use, uncached_impl, line)
    builder.goto(call_func)

    builder.activate_block(call_func)
    gen_calls_to_correct_impl(builder, impl_to_use, arg_info, fitem, line)

