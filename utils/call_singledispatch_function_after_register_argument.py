
def call_singledispatch_function_after_register_argument(ctx: MethodContext) -> Type:
    """Called on the function after passing a type to register"""
    register_callable = ctx.type
    if isinstance(register_callable, Instance):
        type_args = RegisterCallableInfo(*register_callable.args)  # type: ignore[arg-type]
        func = get_first_arg(ctx.arg_types)
        if func is not None:
            register_function(
                ctx, type_args.singledispatch_obj, func, ctx.api.options, type_args.register_type
            )
            # see call to register_function in the callback for register
            return func
    return ctx.default_return_type

