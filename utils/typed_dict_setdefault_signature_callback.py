
def typed_dict_setdefault_signature_callback(ctx: MethodSigContext) -> CallableType:
    """Try to infer a better signature type for TypedDict.setdefault.

    This is used to get better type context for the second argument that
    depends on a TypedDict value type.
    """
    signature = ctx.default_signature
    str_type = ctx.api.named_generic_type("builtins.str", [])
    if (
        isinstance(ctx.type, TypedDictType)
        and len(ctx.args) == 2
        and len(ctx.args[0]) == 1
        and isinstance(ctx.args[0][0], StrExpr)
        and len(signature.arg_types) == 2
        and len(ctx.args[1]) == 1
    ):
        key = ctx.args[0][0].value
        value_type = ctx.type.items.get(key)
        if value_type:
            return signature.copy_modified(arg_types=[str_type, value_type])
    return signature.copy_modified(arg_types=[str_type, signature.arg_types[1]])

