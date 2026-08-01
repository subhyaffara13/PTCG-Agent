
def typed_dict_pop_signature_callback(ctx: MethodSigContext) -> CallableType:
    """Try to infer a better signature type for TypedDict.pop.

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
        and len(signature.variables) == 1
        and len(ctx.args[1]) == 1
    ):
        key = ctx.args[0][0].value
        value_type = ctx.type.items.get(key)
        if value_type:
            # Tweak the signature to include the value type as context. It's
            # only needed for type inference since there's a union with a type
            # variable that accepts everything.
            tv = signature.variables[0]
            assert isinstance(tv, TypeVarType)
            typ = make_simplified_union([value_type, tv])
            return signature.copy_modified(arg_types=[str_type, typ], ret_type=typ)
    return signature.copy_modified(arg_types=[str_type, signature.arg_types[1]])

