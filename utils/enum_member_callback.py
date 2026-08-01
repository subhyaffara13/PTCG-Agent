
def enum_member_callback(ctx: mypy.plugin.FunctionContext) -> Type:
    """By default `member(1)` will be inferred as `member[int]`,
    we want to improve the inference to be `Literal[1]` here."""
    if ctx.arg_types and ctx.arg_types[0]:
        arg = get_proper_type(ctx.arg_types[0][0])
        proper_return = get_proper_type(ctx.default_return_type)
        if (
            isinstance(arg, Instance)
            and arg.last_known_value
            and isinstance(proper_return, Instance)
            and len(proper_return.args) == 1
        ):
            return proper_return.copy_modified(args=[arg])
    return ctx.default_return_type

