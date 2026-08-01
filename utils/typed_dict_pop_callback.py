
def typed_dict_pop_callback(ctx: MethodContext) -> Type:
    """Type check and infer a precise return type for TypedDict.pop."""
    if (
        isinstance(ctx.type, TypedDictType)
        and len(ctx.arg_types) >= 1
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

        value_types = []
        for key in keys:
            if key in ctx.type.required_keys or key in ctx.type.readonly_keys:
                ctx.api.msg.typeddict_key_cannot_be_deleted(ctx.type, key, key_expr)

            value_type = ctx.type.items.get(key)
            if value_type:
                value_types.append(value_type)
            else:
                ctx.api.msg.typeddict_key_not_found(ctx.type, key, key_expr)
                return AnyType(TypeOfAny.from_error)

        if len(ctx.args[1]) == 0:
            return make_simplified_union(value_types)
        elif len(ctx.arg_types) == 2 and len(ctx.arg_types[1]) == 1 and len(ctx.args[1]) == 1:
            return make_simplified_union([*value_types, ctx.arg_types[1][0]])
    return ctx.default_return_type

