
def gen_func_ir(
    builder: IRBuilder,
    args: list[Register],
    blocks: list[BasicBlock],
    sig: FuncSignature,
    fn_info: FuncInfo,
    cdef: ClassDef | None,
    is_singledispatch_main_func: bool = False,
) -> tuple[FuncIR, Value | None]:
    """Generate the FuncIR for a function.

    This takes the basic blocks and function info of a particular
    function and returns the IR. If the function is nested,
    also returns the register containing the instance of the
    corresponding callable class.
    """
    func_reg: Value | None = None
    if fn_info.is_nested or fn_info.in_non_ext:
        func_ir = add_call_to_callable_class(builder, args, blocks, sig, fn_info)
        add_get_to_callable_class(builder, fn_info)
        func_reg = instantiate_callable_class(builder, fn_info)
    else:
        fitem = fn_info.fitem
        assert isinstance(fitem, FuncDef), fitem
        func_decl = builder.mapper.func_to_decl[fitem]
        if cdef and fn_info.name == FAST_PREFIX + func_decl.name:
            # Special-cased version of a method has a separate FuncDecl, use that one.
            func_decl = builder.mapper.type_to_ir[cdef.info].method_decls[fn_info.name]
        if fn_info.is_decorated or is_singledispatch_main_func:
            class_name = None if cdef is None else cdef.name
            func_decl = FuncDecl(
                fn_info.name,
                class_name,
                builder.module_name,
                sig,
                func_decl.kind,
                is_prop_getter=func_decl.is_prop_getter,
                is_prop_setter=func_decl.is_prop_setter,
                is_generator=func_decl.is_generator,
                is_coroutine=func_decl.is_coroutine,
                implicit=func_decl.implicit,
                internal=func_decl.internal,
            )
            func_ir = FuncIR(func_decl, args, blocks, fitem.line, traceback_name=fitem.name)
        else:
            func_ir = FuncIR(func_decl, args, blocks, fitem.line, traceback_name=fitem.name)
    return (func_ir, func_reg)

