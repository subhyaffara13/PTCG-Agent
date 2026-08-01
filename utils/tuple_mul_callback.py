
def tuple_mul_callback(ctx: MethodContext) -> Type:
    """Infer a more precise return type for tuple.__mul__ and tuple.__rmul__.

    This is used to return a specific sized tuple if multiplied by Literal int
    """
    if not isinstance(ctx.type, TupleType):
        return ctx.default_return_type

    arg_type = get_proper_type(ctx.arg_types[0][0])
    if isinstance(arg_type, Instance) and arg_type.last_known_value is not None:
        value = arg_type.last_known_value.value
        if isinstance(value, int):
            return ctx.type.copy_modified(items=ctx.type.items * value)
    elif isinstance(arg_type, LiteralType):
        value = arg_type.value
        if isinstance(value, int):
            return ctx.type.copy_modified(items=ctx.type.items * value)

    return ctx.default_return_type

