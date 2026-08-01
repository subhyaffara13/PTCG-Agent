
def typed_dict_delitem_callback(ctx: MethodContext) -> Type:
    """Type check TypedDict.__delitem__."""
    if (
        isinstance(ctx.type, TypedDictType)
        and len(ctx.arg_types) == 1
        and len(ctx.arg_types[0]) == 1
    ):
        key_expr = ctx.args[0][0]
        keys = try_getting_str_literals(key_expr, ctx.arg_types[0][0])
        if keys is None:
            ctx.api.fail(
                message_registry.TYPEDDICT_KEY_MUST_BE_STRING_LITERAL,
                key_expr,
                code=codes.LITERAL_REQ,
            )
            return AnyType(TypeOfAny.from_error)

        for key in keys:
            if key in ctx.type.required_keys or key in ctx.type.readonly_keys:
                ctx.api.msg.typeddict_key_cannot_be_deleted(ctx.type, key, key_expr)
            elif key not in ctx.type.items:
                ctx.api.msg.typeddict_key_not_found(ctx.type, key, key_expr)
    return ctx.default_return_type

