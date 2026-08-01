
def proper_types_hook(ctx: FunctionContext) -> Type:
    """Check if this get_proper_types() call is not redundant."""
    arg_types = ctx.arg_types[0]
    if arg_types:
        arg_type = arg_types[0]
        proper_type = get_proper_type_instance(ctx)
        item_type = UnionType.make_union([NoneTyp(), proper_type])
        ok_type = ctx.api.named_generic_type("typing.Iterable", [item_type])
        if is_proper_subtype(arg_type, ok_type):
            ctx.api.fail("Redundant call to get_proper_types()", ctx.context)
    return ctx.default_return_type

