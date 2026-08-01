
def proper_type_hook(ctx: FunctionContext) -> Type:
    """Check if this get_proper_type() call is not redundant."""
    arg_types = ctx.arg_types[0]
    if arg_types:
        arg_type = get_proper_type(arg_types[0])
        proper_type = get_proper_type_instance(ctx)
        if is_proper_subtype(arg_type, UnionType.make_union([NoneTyp(), proper_type])):
            # Minimize amount of spurious errors from overload machinery.
            # TODO: call the hook on the overload as a whole?
            if isinstance(arg_type, (UnionType, Instance)):
                ctx.api.fail("Redundant call to get_proper_type()", ctx.context)
    return ctx.default_return_type

