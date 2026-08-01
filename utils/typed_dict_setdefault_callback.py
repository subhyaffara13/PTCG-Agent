
def typed_dict_setdefault_callback(ctx: MethodContext) -> Type:
    """Type check TypedDict.setdefault and infer a precise return type."""
    if (
        isinstance(ctx.type, TypedDictType)
        and len(ctx.arg_types) == 2
        and len(ctx.arg_types[0]) == 1
        and len(ctx.arg_types[1]) == 1
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

        assigned_readonly_keys = ctx.type.readonly_keys & set(keys)
        if assigned_readonly_keys:
            ctx.api.msg.readonly_keys_mutated(assigned_readonly_keys, context=key_expr)

        default_type = ctx.arg_types[1][0]
        default_expr = ctx.args[1][0]

        value_types = []
        for key in keys:
            value_type = ctx.type.items.get(key)

            if value_type is None:
                ctx.api.msg.typeddict_key_not_found(ctx.type, key, key_expr)
                return AnyType(TypeOfAny.from_error)

            # The signature_callback above can't always infer the right signature
            # (e.g. when the expression is a variable that happens to be a Literal str)
            # so we need to handle the check ourselves here and make sure the provided
            # default can be assigned to all key-value pairs we're updating.
            if not is_subtype(default_type, value_type):
                ctx.api.msg.typeddict_setdefault_arguments_inconsistent(
                    default_type, value_type, default_expr
                )
                return AnyType(TypeOfAny.from_error)

            value_types.append(value_type)

        return make_simplified_union(value_types)
    return ctx.default_return_type

