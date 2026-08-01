
def singledispatch_register_callback(ctx: MethodContext) -> Type:
    """Called for functools._SingleDispatchCallable.register"""
    assert isinstance(ctx.type, Instance)
    # TODO: check that there's only one argument
    first_arg_type = get_proper_type(get_first_arg(ctx.arg_types))
    if isinstance(first_arg_type, (CallableType, Overloaded)) and first_arg_type.is_type_obj():
        # HACK: We received a class as an argument to register. We need to be able
        # to access the function that register is being applied to, and the typeshed definition
        # of register has it return a generic Callable, so we create a new
        # SingleDispatchRegisterCallable class, define a __call__ method, and then add a
        # plugin hook for that.

        # is_subtype doesn't work when the right type is Overloaded, so we need the
        # actual type
        register_type = first_arg_type.items[0].get_instance_type()
        type_args = RegisterCallableInfo(register_type, ctx.type)
        register_callable = make_fake_register_class_instance(ctx.api, type_args)
        return register_callable
    elif isinstance(first_arg_type, CallableType):
        # TODO: do more checking for registered functions
        register_function(ctx, ctx.type, first_arg_type, ctx.api.options)
        # The typeshed stubs for register say that the function returned is Callable[..., T], even
        # though the function returned is the same as the one passed in. We return the type of the
        # function so that mypy can properly type check cases where the registered function is used
        # directly (instead of through singledispatch)
        return first_arg_type

    # fallback in case we don't recognize the arguments
    return ctx.default_return_type

