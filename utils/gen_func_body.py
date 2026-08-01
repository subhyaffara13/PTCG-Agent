
def gen_func_body(
    builder: IRBuilder, sig: FuncSignature, cdef: ClassDef | None, is_singledispatch: bool
) -> tuple[FuncIR, Value | None]:
    load_env_registers(builder)
    gen_arg_defaults(builder)
    if builder.fn_info.contains_nested:
        finalize_env_class(builder)
    add_vars_to_env(builder)
    builder.accept(builder.fn_info.fitem.body)
    builder.maybe_add_implicit_return()

    # Hang on to the local symbol table for a while, since we use it
    # to calculate argument defaults below.
    symtable = builder.symtables[-1]

    args, _, blocks, ret_type, fn_info = builder.leave()

    func_ir, func_reg = gen_func_ir(builder, args, blocks, sig, fn_info, cdef, is_singledispatch)

    # Evaluate argument defaults in the surrounding scope, since we
    # calculate them *once* when the function definition is evaluated.
    calculate_arg_defaults(builder, fn_info, func_reg, symtable)
    return func_ir, func_reg

