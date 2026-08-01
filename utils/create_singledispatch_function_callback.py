
def create_singledispatch_function_callback(ctx: FunctionContext) -> Type:
    """Called for functools.singledispatch"""
    func_type = get_proper_type(get_first_arg(ctx.arg_types))
    if isinstance(func_type, CallableType):
        if len(func_type.arg_kinds) < 1:
            fail(
                ctx, "Singledispatch function requires at least one argument", func_type.definition
            )
            return ctx.default_return_type

        elif not func_type.arg_kinds[0].is_positional(star=True):
            fail(
                ctx,
                "First argument to singledispatch function must be a positional argument",
                func_type.definition,
            )
            return ctx.default_return_type

        # singledispatch returns an instance of functools._SingleDispatchCallable according to
        # typeshed
        singledispatch_obj = get_proper_type(ctx.default_return_type)
        assert isinstance(singledispatch_obj, Instance)
        singledispatch_obj.args += (func_type,)

    return ctx.default_return_type

