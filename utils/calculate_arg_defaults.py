
def calculate_arg_defaults(
    builder: IRBuilder,
    fn_info: FuncInfo,
    func_reg: Value | None,
    symtable: dict[SymbolNode, SymbolTarget],
) -> None:
    """Calculate default argument values and store them.

    They are stored in statics for top level functions and in
    the function objects for nested functions (while constants are
    still stored computed on demand).
    """
    fitem = fn_info.fitem
    for arg in fitem.arguments:
        # Constant values don't get stored but just recomputed
        if arg.initializer and not is_constant(arg.initializer):
            value = builder.coerce(
                builder.accept(arg.initializer), symtable[arg.variable].type, arg.line
            )
            if not fn_info.is_nested:
                name = fitem.fullname + "." + arg.variable.name
                builder.add(InitStatic(value, name, builder.module_name))
            else:
                assert func_reg is not None
                builder.add(SetAttr(func_reg, arg.variable.name, value, arg.line))

