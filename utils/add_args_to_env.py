
def add_args_to_env(
    builder: IRBuilder,
    local: bool = True,
    base: FuncInfo | ImplicitClass | None = None,
    reassign: bool = True,
    prefix: str = "",
) -> None:
    fn_info = builder.fn_info
    args = fn_info.fitem.arguments
    nb = num_bitmap_args(builder, args)
    if local:
        for arg in args:
            rtype = builder.type_to_rtype(arg.variable.type)
            builder.add_local_reg(arg.variable, rtype, is_arg=True)
        for i in reversed(range(nb)):
            builder.add_local_reg(Var(bitmap_name(i)), bitmap_rprimitive, is_arg=True)
    else:
        for arg in args:
            if (
                is_free_variable(builder, arg.variable)
                or fn_info.is_generator
                or fn_info.is_coroutine
            ):
                rtype = builder.type_to_rtype(arg.variable.type)
                assert base is not None, "base cannot be None for adding nonlocal args"
                builder.add_var_to_env_class(
                    arg.variable, rtype, base, reassign=reassign, prefix=prefix
                )

