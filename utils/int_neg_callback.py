
def int_neg_callback(ctx: MethodContext, multiplier: int = -1) -> Type:
    """Infer a more precise return type for int.__neg__ and int.__pos__.

    This is mainly used to infer the return type as LiteralType
    if the original underlying object is a LiteralType object.
    """
    if isinstance(ctx.type, Instance) and ctx.type.last_known_value is not None:
        value = ctx.type.last_known_value.value
        fallback = ctx.type.last_known_value.fallback
        if isinstance(value, int):
            if is_literal_type_like(ctx.api.type_context[-1]):
                return LiteralType(value=multiplier * value, fallback=fallback)
            else:
                return ctx.type.copy_modified(
                    last_known_value=LiteralType(
                        value=multiplier * value,
                        fallback=fallback,
                        line=ctx.type.line,
                        column=ctx.type.column,
                    )
                )
    elif isinstance(ctx.type, LiteralType):
        value = ctx.type.value
        fallback = ctx.type.fallback
        if isinstance(value, int):
            return LiteralType(value=multiplier * value, fallback=fallback)
    return ctx.default_return_type

