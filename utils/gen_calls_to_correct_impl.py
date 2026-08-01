
def gen_calls_to_correct_impl(
    builder: IRBuilder, impl_to_use: Value, arg_info: ArgInfo, fitem: FuncDef, line: int
) -> None:
    current_func_decl = builder.mapper.func_to_decl[fitem]

    def gen_native_func_call_and_return(fdef: FuncDef) -> None:
        func_decl = builder.mapper.func_to_decl[fdef]
        ret_val = builder.builder.call(
            func_decl, arg_info.args, arg_info.arg_kinds, arg_info.arg_names, line
        )
        coerced = builder.coerce(ret_val, current_func_decl.sig.ret_type, line)
        builder.add(Return(coerced))

    int_type_obj = builder.load_builtin("builtins.int", line)
    assert int_type_obj
    is_int = builder.builder.type_is_op(impl_to_use, int_type_obj, line)

    native_call, non_native_call = BasicBlock(), BasicBlock()
    builder.add_bool_branch(is_int, native_call, non_native_call)
    builder.activate_block(native_call)

    passed_id = builder.add(Unbox(impl_to_use, int_rprimitive, line))

    native_ids = get_native_impl_ids(builder, fitem)
    for impl, i in native_ids.items():
        call_impl, next_impl = BasicBlock(), BasicBlock()

        current_id = builder.load_int(i)
        cond = builder.binary_op(passed_id, current_id, "==", line)
        builder.add_bool_branch(cond, call_impl, next_impl)

        # Call the registered implementation
        builder.activate_block(call_impl)

        gen_native_func_call_and_return(impl)
        builder.activate_block(next_impl)

    # We've already handled all the possible integer IDs, so we should never get here
    builder.add(Unreachable())

    builder.activate_block(non_native_call)
    ret_val = builder.py_call(
        impl_to_use, arg_info.args, line, arg_info.arg_kinds, arg_info.arg_names
    )
    coerced = builder.coerce(ret_val, current_func_decl.sig.ret_type, line)
    builder.add(Return(coerced))

