
def typed_dict_get_signature_callback(ctx: MethodSigContext) -> CallableType:
    """Try to infer a better signature type for TypedDict.get.

    This is used to get better type context for the second argument that
    depends on a TypedDict value type.
    """
    signature = ctx.default_signature
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
        value_type = get_proper_type(ctx.type.items.get(key))
        ret_type = signature.ret_type
        if value_type:
            default_arg = ctx.args[1][0]
            if (
                isinstance(value_type, TypedDictType)
                and isinstance(default_arg, DictExpr)
                and len(default_arg.items) == 0
            ):
                # Caller has empty dict {} as default for typed dict.
                value_type = value_type.copy_modified(required_keys=set())
            # Tweak the signature to include the value type as context. It's
            # only needed for type inference since there's a union with a type
            # variable that accepts everything.
            tv = signature.variables[0]
            assert isinstance(tv, TypeVarType)
            return signature.copy_modified(
                arg_types=[signature.arg_types[0], make_simplified_union([value_type, tv])],
                ret_type=ret_type,
            )
    return signature

