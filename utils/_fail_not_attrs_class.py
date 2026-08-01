
def _fail_not_attrs_class(ctx: mypy.plugin.FunctionSigContext, t: Type, parent_t: Type) -> None:
    t_name = format_type_bare(t, ctx.api.options)
    if parent_t is t:
        msg = (
            f'Argument 1 to "evolve" has a variable type "{t_name}" not bound to an attrs class'
            if isinstance(t, TypeVarType)
            else f'Argument 1 to "evolve" has incompatible type "{t_name}"; expected an attrs class'
        )
    else:
        pt_name = format_type_bare(parent_t, ctx.api.options)
        msg = (
            f'Argument 1 to "evolve" has type "{pt_name}" whose item "{t_name}" is not bound to an attrs class'
            if isinstance(t, TypeVarType)
            else f'Argument 1 to "evolve" has incompatible type "{pt_name}" whose item "{t_name}" is not an attrs class'
        )

    ctx.api.fail(msg, ctx.context)

