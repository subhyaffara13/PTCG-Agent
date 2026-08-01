
def gen_dispatch_func_ir(
    builder: IRBuilder, fitem: FuncDef, main_func_name: str, dispatch_name: str, sig: FuncSignature
) -> tuple[FuncIR, Value]:
    """Create a dispatch function (a function that checks the first argument type and dispatches
    to the correct implementation)
    """
    builder.enter(FuncInfo(fitem, dispatch_name))
    setup_callable_class(builder)
    builder.fn_info.callable_class.ir.attributes["registry"] = dict_rprimitive
    builder.fn_info.callable_class.ir.attributes["dispatch_cache"] = dict_rprimitive
    builder.fn_info.callable_class.ir.has_dict = True
    builder.fn_info.callable_class.ir.needs_getseters = True
    generate_singledispatch_callable_class_ctor(builder)

    generate_singledispatch_dispatch_function(builder, main_func_name, fitem)
    args, _, blocks, _, fn_info = builder.leave()
    dispatch_callable_class = add_call_to_callable_class(builder, args, blocks, sig, fn_info)
    builder.functions.append(dispatch_callable_class)
    add_get_to_callable_class(builder, fn_info)
    add_register_method_to_callable_class(builder, fn_info)
    func_reg = instantiate_callable_class(builder, fn_info)
    dispatch_func_ir = generate_dispatch_glue_native_function(
        builder, fitem, dispatch_callable_class.decl, dispatch_name
    )

    return dispatch_func_ir, func_reg

