
def add_call_to_callable_class(
    builder: IRBuilder,
    args: list[Register],
    blocks: list[BasicBlock],
    sig: FuncSignature,
    fn_info: FuncInfo,
) -> FuncIR:
    """Generate a '__call__' method for a callable class representing a nested function.

    This takes the blocks and signature associated with a function
    definition and uses those to build the '__call__' method of a
    given callable class, used to represent that function.
    """
    # Since we create a method, we also add a 'self' parameter.
    nargs = len(sig.args) - sig.num_bitmap_args
    sig = FuncSignature(
        (RuntimeArg(SELF_NAME, object_rprimitive),) + sig.args[:nargs], sig.ret_type
    )
    call_fn_decl = FuncDecl("__call__", fn_info.callable_class.ir.name, builder.module_name, sig)
    call_fn_ir = FuncIR(
        call_fn_decl, args, blocks, fn_info.fitem.line, traceback_name=fn_info.fitem.name
    )
    fn_info.callable_class.ir.methods["__call__"] = call_fn_ir
    fn_info.callable_class.ir.method_decls["__call__"] = call_fn_decl
    return call_fn_ir

