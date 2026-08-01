
def add_helper_to_generator_class(
    builder: IRBuilder, arg_regs: list[Register], blocks: list[BasicBlock], fn_info: FuncInfo
) -> FuncDecl:
    """Generates a helper method for a generator class, called by '__next__' and 'throw'."""
    helper_fn_decl = fn_info.generator_class.ir.method_decls[GENERATOR_HELPER_NAME]
    helper_fn_ir = FuncIR(
        helper_fn_decl, arg_regs, blocks, fn_info.fitem.line, traceback_name=fn_info.fitem.name
    )
    fn_info.generator_class.ir.methods[GENERATOR_HELPER_NAME] = helper_fn_ir
    builder.functions.append(helper_fn_ir)
    fn_info.env_class.env_user_function = helper_fn_ir

    return helper_fn_decl

