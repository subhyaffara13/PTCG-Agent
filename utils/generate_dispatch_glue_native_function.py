
def generate_dispatch_glue_native_function(
    builder: IRBuilder, fitem: FuncDef, callable_class_decl: FuncDecl, dispatch_name: str
) -> FuncIR:
    line = fitem.line
    builder.enter()
    # We store the callable class in the globals dict for this function
    callable_class = builder.load_global_str(dispatch_name, line)
    decl = builder.mapper.func_to_decl[fitem]
    arg_info = get_args(builder, decl.sig.args, line)
    args = [callable_class] + arg_info.args
    arg_kinds = [ArgKind.ARG_POS] + arg_info.arg_kinds
    arg_names = arg_info.arg_names
    arg_names.insert(0, "self")
    ret_val = builder.builder.call(callable_class_decl, args, arg_kinds, arg_names, line)
    builder.add(Return(ret_val))
    arg_regs, _, blocks, _, fn_info = builder.leave()
    return FuncIR(decl, arg_regs, blocks)

