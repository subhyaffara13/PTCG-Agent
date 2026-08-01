
def isinstance_proper_hook(ctx: FunctionContext) -> Type:
    if len(ctx.arg_types) != 2 or not ctx.arg_types[1]:
        return ctx.default_return_type

    right = get_proper_type(ctx.arg_types[1][0])
    for arg in ctx.arg_types[0]:
        if (
            is_improper_type(arg) or isinstance(get_proper_type(arg), AnyType)
        ) and is_dangerous_target(right):
            if is_special_target(right):
                return ctx.default_return_type
            ctx.api.fail(
                "Never apply isinstance() to unexpanded types;"
                " use mypy.types.get_proper_type() first",
                ctx.context,
            )
            ctx.api.note(  # type: ignore[attr-defined]
                "If you pass on the original type"
                " after the check, always use its unexpanded version",
                ctx.context,
            )
    return ctx.default_return_type

