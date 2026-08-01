
def len_callback(ctx: FunctionContext) -> Type:
    """Infer a better return type for 'len'."""
    if len(ctx.arg_types) == 1 and len(ctx.arg_types[0]) == 1:
        arg_type = ctx.arg_types[0][0]
        arg_type = get_proper_type(arg_type)
        if isinstance(arg_type, Instance) and arg_type.type.fullname == "librt.vecs.vec":
            # The length of vec is a fixed-width integer, for more
            # low-level optimization potential.
            return ctx.api.named_generic_type("mypy_extensions.i64", [])
    return ctx.default_return_type

