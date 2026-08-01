
def partial_new_callback(ctx: mypy.plugin.FunctionContext) -> Type:
    """Infer a more precise return type for functools.partial"""
    if not isinstance(ctx.api, mypy.checker.TypeChecker):  # use internals
        return ctx.default_return_type
    if len(ctx.arg_types) != 3:  # fn, *args, **kwargs
        return ctx.default_return_type
    if len(ctx.arg_types[0]) != 1:
        return ctx.default_return_type

    if isinstance(get_proper_type(ctx.arg_types[0][0]), Overloaded):
        # TODO: handle overloads, just fall back to whatever the non-plugin code does
        return ctx.default_return_type
    return handle_partial_with_callee(ctx, callee=ctx.arg_types[0][0])

